% Define the number of threads (bar plots) and the size of the data queue
num_threads = 4;
queue_size = 2;

% Create a controller to assign data to threads
data_controller = parallel.pool.DataQueue;

% Create a queue for processed data
result_queue = parallel.pool.DataQueue;

% Create a parallel pool with the specified number of workers
pool = parpool('local', num_threads);

% Initialize the bar plots (you can customize this part as needed)
figure;
barHandles = bar(zeros(1, num_threads));
title('Parallel Bar Plots');

% Define a function for processing data in each thread
processingFunction = @(data) process_data(data);

% Start listening to the data controller
afterEach(data_controller, num_threads, @(~) update_bar_plots(barHandles));

% Start processing data in parallel
parfor i = 1:num_threads
    while true
        data = data_controller.pop();
        if isempty(data)
            break; % Exit the loop when no more data is available
        end
        processed_data = processingFunction(data);
        result_queue.push(processed_data);
    end
end

% Delete the parallel pool and close the figure when done
delete(pool);
close(gcf);

% Define the processing function (customize this for your specific data processing)
function result = process_data(data)
    % Placeholder processing, you should replace this with your actual processing code
    pause(rand); % Simulate processing time
    result = data * 2;
end

% Update the bar plots with the latest data
function update_bar_plots(barHandles)
    % Get data from the result queue and update the bar plots
    while true
        processed_data = result_queue.pop();
        if isempty(processed_data)
            break; % Exit the loop when no more data is available
        end
        % Update the corresponding bar plot with processed data
        barHandles.Value = processed_data;
    end
end
