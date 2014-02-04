classdef FoosGame
    properties 
        NUM_FOOSPLAYERS = 26;
        NUM_FIELDED = 22;
        ITER_PER_QUARTER = 200;
    
        MAX_MESSAGE_LENGTH = 1024;
        DELIMITER = ' ';

        game_state = [];
        comm = ''
    end
    methods
        function obj = FoosGame(GAMEID)
            obj.comm = tcpip('crisco.seas.harvard.edu', 8080);
            fopen(obj.comm);

            game_i = num2str(GAMEID); 
            fwrite(obj.comm, game_i);

            while obj.comm.BytesAvailable == 0 end
            data = fread(obj.comm, obj.comm.BytesAvailable, 'char');
            game_id = sprintf('%s', data);
            
            fprintf(['Waiting for game ' game_id '\n'])

            while obj.comm.BytesAvailable == 0 end
            data = fread(obj.comm, obj.comm.BytesAvailable, 'char');
            ready_msg = sprintf('%s', data);

            fprintf([ready_msg '\n'])
            obj.game_state = [0; 0; 0; 0];
        end
        function delete(obj)
            fclose(obj.comm)
        end
        
        % -------------------------------------
        function valid = is_valid(obj, move)
            % Makes sense as a roster
            if length(move) ~= obj.NUM_FOOSPLAYERS
                valid = false;
                return;
            end

            % Has exactly NUM_FIELDED players on the field
            if sum((abs(move)<5)) ~= obj.NUM_FIELDED
                valid = false;
                return;
            end
            
            % If this is a new quarter, then any fielded roster is ok
            if mod(obj.game_state(3), obj.ITER_PER_QUARTER) == 0
                valid = true;
                return;
            end

            % Else we're mid-quarter and can only move one player to an adjacent row
            player_pos = obj.game_state(5:(5+obj.NUM_FOOSPLAYERS));
            valid = (sum(abs(player_pos-move)) <= 1);
           return;
        end
        
        % --------------------------------------------------
        function game_state = make_move(obj, move)
            %Check if this is a valid move and display a warning
            if ~obj.is_valid(move)
                fprintf('**WARNING!! SUBMITTING INVALID MOVE**\n')
            end

            move_string = mat2str(move);
            move_string = move_string(2:end-1);
            fprintf(['Sending: ' move_string '\n']);
            
            fwrite(obj.comm, move_string);
            while obj.comm.BytesAvailable == 0 end
            data = fread(obj.comm, obj.comm.BytesAvailable, 'char');
            message = sprintf('%s', data);

            fprintf(['Recieving: ' message '\n']);
            if ~data
                fprintf('GAME KILLED\n')
                exit
            end

            game_state = str2num(message);
        end
    
    end   % END OF METHODS
    
    
end