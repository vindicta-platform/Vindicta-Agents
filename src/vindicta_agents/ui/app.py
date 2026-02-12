import chainlit as cl
from vindicta_agents.swarm.nexus import vindicta_swarm
from vindicta_agents.swarm.state import VindictaState
import uuid

@cl.on_chat_start
async def start():
    # Use a unique thread ID for this session
    thread_id = str(uuid.uuid4())
    cl.user_session.set("thread_id", thread_id)
    
    await cl.Message(
        content="**Vindicta Swarm Link Established.**\n\nI am the Nexus. State your intent to begin the architectural protocol.",
        author="Nexus"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    thread_id = cl.user_session.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}
    
    # Identify if we are resuming or starting new
    # For now, simple flow: User input -> Intent -> Planning -> Review -> Execution
    
    inputs = {
        "intent": message.content,
    }

    msg = cl.Message(content="", author="Swarm")
    await msg.send()
    
    # 1. Start execution (up to interrupt)
    # stream_mode="updates" gives us the outputs of the nodes that just ran
    async for event in vindicta_swarm.astream(inputs, config=config, stream_mode="updates"):
        for node_name, state_update in event.items():
            if "execution_log" in state_update:
                for log in state_update["execution_log"]:
                    await msg.stream_token(f"> **{node_name}**: {log}\n")
            
            # Show spec/plan updates if available (usually from Meta-Agents)
            if "spec_content" in state_update and state_update["spec_content"]:
                 await cl.Message(
                     content=f"**Spec Generated**", 
                     elements=[cl.Text(name="Spec", content=state_update["spec_content"], display="inline", language="markdown")],
                     author=node_name
                 ).send()

            if "plan_content" in state_update and state_update["plan_content"]:
                 await cl.Message(
                     content=f"**Plan Generated**", 
                     elements=[cl.Text(name="Plan", content=state_update["plan_content"], display="inline", language="markdown")],
                     author=node_name
                 ).send()

    await msg.update()

    # 2. Check for Interrupt (Human Review)
    snapshot = vindicta_swarm.get_state(config)
    if snapshot.next and "ExecutionPhase" in snapshot.next:
        # Retrieve plan and tasks from the compiled state
        state = snapshot.values
        plan = state.get("plan_content", "")
        tasks = state.get("tasks", [])
        
        # Display Plan Summary
        await cl.Message(
            content=f"**Planning Phase Complete.**\nProposed {len(tasks)} tasks for execution.",
            author="Nexus"
        ).send()
        
        # Ask for approval using Actions
        actions = [
            cl.Action(name="approve", value="yes", label="Approve & Execute"),
            cl.Action(name="reject", value="no", label="Reject & Refine")
        ]
        
        res = await cl.AskActionMessage(
            content="Do you authorize execution of this plan?",
            actions=actions,
            timeout=600
        ).send()
        
        if res and res.get("value") == "yes":
            await cl.Message(content="**Authorization Code Accepted.** Initiating execution protocol...", author="Nexus").send()
            
            # Resume Execution (pass None to resume)
            execution_msg = cl.Message(content="", author="Swarm Execution")
            await execution_msg.send()
            
            # Resume
            async for event in vindicta_swarm.astream(None, config=config, stream_mode="updates"):
                for node_name, state_update in event.items():
                    if "execution_log" in state_update:
                        for log in state_update["execution_log"]:
                            await execution_msg.stream_token(f"> **{node_name}**: {log}\n")
            
            await execution_msg.update()
            await cl.Message(content="**Protocol Complete.**", author="Nexus").send()
            
        else:
            await cl.Message(content="**Authorization Denied.** Resetting protocol.", author="Nexus").send()
