$(document).ready(function() {
    function fetchUpdates() {
        $.ajax({
            url: '/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // update the invitations
                var invitesList = $('#invites ul');
                invitesList.empty();
                data.invitations.forEach(function(invitation) {
                    invitesList.append('<li>' + invitation.from_user.username + ' has invited you to a game! <a href="/accept_invitation/' + invitation.id + '/" class="accept-invite">Accept</a> | <a href="/reject_invitation/' + invitation.id + '/" class="reject-invite">Reject</a></li>');
                });

                // update the game list
                var gamesList = $('#active-games ul');
                gamesList.empty();
                data.games_with_opponent.forEach(function(game) {
                    gamesList.append('<li><a href="/game/' + game.game.id + '">Game with ' + game.opponent.username + '</a></li>');
                });
            }
        });
    }

    // check and fetch updates every second
    setInterval(fetchUpdates, 1000);

    // handle the accept invite link
    $(document).on('click', '.accept-invite', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            type: 'GET',
            success: function(response) {
                if (response.redirect) {
                    window.location.href = response.url;
                }
            }
        });
    });

    // handle the reject link
    $(document).on('click', '.reject-invite', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            type: 'GET',
            success: function() {
                fetchUpdates();
            }
        });
    });

    // handle the send invite form
    $('#send-invite-form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),
            success: function() {
                form.find('input[name="username"]').val('');
                fetchUpdates();
            }
        });
    });
});
