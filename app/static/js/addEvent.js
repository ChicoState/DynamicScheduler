function radio_click(r) {
    //is_task=
    if(r.value == "true") {
        //disable mandating: from_time, to_time
        document.getElementById("from_time").required = false; //when a task, no need for event stuff
        document.getElementById("to_time").required = false; //when a task, no need for event stuff
    }
    if(r.value == "false") {
        //enable mandating: from_time, to_time
        document.getElementById("from_time").required = true; //required for an event
        document.getElementById("to_time").required = true; //required for an event
    }
}