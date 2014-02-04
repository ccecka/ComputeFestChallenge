%% SKELETON GAME FOR MATLAB

% USAGE foosgame(GAMEID)
% GAMEID = 0    creates a new game
% GAMEID = WXYZ connect to a specific game

function [] = foosteam(GAMEID)
    global NUM_FOOSPLAYERS;
    global NUM_FIELDED;
    global ITER_PER_QUARTER;

    NUM_FOOSPLAYERS = 26;
    NUM_FIELDED = 22;
    ITER_PER_QUARTER = 200;

    % Connect to a FoosGame with id from the command line
    game = FoosGame(GAMEID);

    % Initial roster - defense!
    roster = -4 * ones(1, NUM_FOOSPLAYERS);
    roster(1:4) = [100,100,100,100];

    while true
        % Send the roster and get the game state
        game_state = game.make_move(roster);
        if game_state(3) == 4 * ITER_PER_QUARTER
           break;
        end

        % Use the game state to determine the next move
        roster = new_move(game_state);
    end

    fprintf(['Final Score: ' int2str(game_state(1)) ' - ' int2str(game_state(2)) '\n']);
    if game_state(1) > game_state(2)
        fprintf('WIN!\n');
    end
    if game_state(1) == game_state(2)
        fprintf('Tie Game\n');
    end

function roster = new_move(game_state)
    global NUM_FOOSPLAYERS;
    %% Determine a roster for the next round from the current game state.
    % Input:
    % game_state(1): team score
    % game_state(2): opponent team score
    % game_state(3): game round number
    % game_state(4): row number of the ball
    % game_state( 5:30 ): team foosplayer row positions
    % game_state(31:56 ]: team foosplayer fatigues
    % game_state(57:82 ): opponent foosplayer row positions
    % game_state(83:108): opponent foosplayer fatigues
    % Output:
    % roster(1:NUM_FOOSPLAYERS): team foosplayer row positions for next round

    % Trivial strategy, null move
    roster = game_state(5:30);
    return;
