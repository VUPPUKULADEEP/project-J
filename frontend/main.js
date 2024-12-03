$(document).ready(function () {



    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
      });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    // mic button click event

    $("#MicBtn").click(function () { 
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.start_listening()
    });


    function sendInputToPython() {
        const input = $("#inputdata").val().trim(); // Get user input and trim whitespace
        if (input) { // Ensure input is not empty
            console.log("Sending input to Python:", input);
            $("#inputdata").val('')
            eel.sending(input); // Call Python function
        }
    }
    eel.expose(i)
    function i(){
    // Add event listener for the "Enter" key
    $("#inputdata").on("keydown", function (event) {
        if (event.key === "Enter") { // Check if "Enter" key is pressed
            sendInputToPython(); // Call the function to send input
        }
    });
}
});