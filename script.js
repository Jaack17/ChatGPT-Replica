$(document).ready(function() {
    // Function to send message to the backend and display bot response
    function sendMessage() {
        // Get the user input
        var userInput = $('#user-input').val();

        // Clear the input field
        $('#user-input').val('');

        // Display user message in the chat interface
        $('#messages').append('<div class="message user-message"><strong>You:</strong> ' + userInput + '</div>');

        // Send the user input to the backend and receive response
        $.ajax({
            type: 'POST',
            url: '/message',
            contentType: 'application/json',
            data: JSON.stringify({ message: userInput }),
            success: function(data) {
                // Display bot's response in the chat interface
                $('#messages').append('<div class="message bot-message"><strong>ChatGPT:</strong> ' + data.message + '</div>');

                // Scroll to the bottom of the chat container
                $('#messages').scrollTop($('#messages')[0].scrollHeight);
            }
        });
    }

    // Event listener for send button click
    $('#send-btn').click(function() {
        sendMessage();
    });

    // Event listener for pressing Enter key in the input field
    $('#user-input').keypress(function(e) {
        if (e.which == 13) { // Enter key code
            sendMessage();
        }
    });
});
