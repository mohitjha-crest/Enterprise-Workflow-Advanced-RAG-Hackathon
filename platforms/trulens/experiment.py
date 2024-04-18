from trulens_eval.tru_virtual import TruVirtual, VirtualApp, VirtualRecord
from trulens_eval import Select
from feedback_function import create_feedback_functions
from time import sleep
from dotenv import load_dotenv

from platforms.vectara_platform.vectara import request_vectara
from platforms.openai.openai import get_output

load_dotenv()

def run_experiment():

    virtual_app = dict(
        llm=dict(
            modelname="Vectara Boomerang Model"
        ),
        template="Information about the template I used in my app",
        debug="All of these fields are completely optional"
    )

    virtual_app = VirtualApp(virtual_app)  # can start with the prior dictionary
    virtual_app[Select.RecordCalls.llm.maxtokens] = 1024

    retriever = Select.RecordCalls.retriever
    synthesizer = Select.RecordCalls.synthesizer

    virtual_app[retriever] = "retriever"
    virtual_app[synthesizer] = "synthesizer"

    # The selector for a presumed context retrieval component's call to
    # `get_context`. The names are arbitrary but may be useful for readability on
    # your end.
    context_call = retriever.get_context
    generation = synthesizer.generate

    questions = ['My windows VM is getting powered off again and again','My windows VM machines power is fluctuate', 'While connection CDS',
    'My windows VM machines power is fluctuate', "While connection CDS, It's shows your password is expired", "I'm trying to connect CDS but it shows your password is expired", "While connection CDS wifi, It's shows your password is expired", "I'm trying to connect CDS wifi but it shows your password is expired", 'Not able to ssh in production VM', 'Not able to ssh in production VM. Could you please help?', 'Not able to connect GP', 'Not able to connect Global Protect', 'Not able to connect after passwored chnage', "I have chnaged my password but now I'm not able to connect", 'Not able to pwoer off my VM using VMT', 'Not able to power on my VM usinf VMT', "Not able to connect Jira when i'm connected with Global Protect", "Not able to connect confluence when i'm connected with GP", 'Not able to open HRMS in my MacBook device', 'Not able to access Jira in MacBook', 'Not able to login my splunk okta', 'Not able to acces my splunk mail', "I'm facing slo performance in VM 1.2.3.4", 'VM 1.2.3.4 is performing slow', 'Vm 1.2.3.4 is running slow', 'Not able to clone repo from bitbucket', 'Not able to access teamplanner', 'Not able to open teamplanner', 'Internet is periodically disconnecting', 'Internet is disconnecting rapidly', 'Not able to Proxy', 'Proxy is not working', 'Not able to acces gmail on mobile', 'Could you please help to setup okta on my new mobile', 'Help me to reconfigure okta in my new device', 'Not able to access roster', 'Roster is not accessible from my device', 'Could you please help to setup DUO on my new mobile', 'Help me to reconfigure DUO in my new device', 'Speaker is not worling in my device', 'Microphone is not working properly in my device', 'Help me to change password in my Macbook', 'How to change password in Macbook', 'Not able connect VM 1.2.3.4', 'Not able to shh in VM 1.2.3.4', 'Not able to ssh AWS EC2 instance 1.2.3.4', 'Not avle to connect EC2 instance 1.2.3.4', 'Not able to connect VPN', 'Not able to connect forticlient VPN', 'Not able to open JIRA even though connected to a VPN', "I'm connected to VPN but still not able to open Jira", 'Not able to connect CDS wifi',
                 'Not able to login in Confluence', 'Not able to login in Jira', 'Not able to access UI using port 8000 in VM', "I'm trying to access UI using port 8000 in my VM. but not able to access.", 'Not able to acces VMT', 'Not able to open VMT toll', 'Not able to access Jira', 'Not able to open JIRA', 'Not able to access Confluence page', 'Not able to open Confluence', 'Not able to acces AWS SSO', 'Not able to access Crest University', 'Not able to open Cres Uni.', 'Not able to turn on my device', 'My device is not getting power on', 'My Macbook is not performing well', 'My Macbook is not working properly', 'My laptop touchpad is not working', 'Touchpad of my laptop is not working properly', 'Not able to access any splunk tools after connection GP', 'Not able to access any splunk tools after connection Global Protect', 'My charger is not working', 'My laptop charger is not working', 'Jira is not working properly', 'Jira is not working in my device', 'Internet is very slow in 4th floor', 'Low internet speed at 5th floor', 'My macbook getting restart automatically', 'Can you please provide public IP address of crest network', 'Provide list of public ips of crest network', 'My macbook is not getting start after the update', "I've update my macbook and now i'm not able to start my macbook", 'Slow internet slpped in VM 1.2.3.4', 'Facing slow internet speed in my VM 1.2.3.4', 'internet is nor working after connecting to Global Protect', 'Please provide credentials of the amazon security lake plugin for testing purposes', 'Need credentials of the amazon security lake plugin', 'Internet speed is running slow in my Mac device', 'Facing internet issue in Macbook', 'Not able to ssh VM into VSCode', 'Please provide ateps to ssh VM in VSCode', 'Not able to create fork from git', 'My keyboard is not working properly', 'facing issue in my keyboard', 'How to archive Jira project?', 'Not able to login in jira after changing my password', 'Could you please help me to configure Global Protect in my splunk macbook', 'How to setup Global Protect VPN in splunk Macbook?', 'My AD password got expired. How to change my AD password?', 'How to change my expired AD password?']
    data = []

    for query in questions:
        output_result = request_vectara(query)

        context_ = output_result['responseSet'][0]['response'][0]['text']
        output_result = get_output(context=context_, query=query)
        print("***************** ", output_result, "*********************")
        rec = VirtualRecord(
            main_input=query,
            main_output=output_result,
            calls={
                context_call: dict(
                    args=[query],
                    rets=[context_]
                ),
            }
        )
        data.append(rec)

    print("######################### ", data)

    # Select context to be used in feedback. We select the return values of the
    # virtual `get_context` call in the virtual `retriever` component. Names are
    # arbitrary except for `rets`.
    context = context_call.rets[:]

    virtual_recorder = TruVirtual(
        app_id="Experiment: RAG over SOP + History Chat using Vectara + gpt-3.5-turbo",
        app=virtual_app,
        feedbacks=create_feedback_functions(context=context),
    )

    for record in data:
        virtual_recorder.add_record(record)
        sleep(13)

    print("Experiment executed successfully")
    return True
