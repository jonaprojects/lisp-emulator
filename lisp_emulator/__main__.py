from common_lisp import *
def main():
    """ The main method."""
    intro_font = Figlet(font='standard')
    print(intro_font.renderText('LISPER '), end='')
    print('Version 1.0.2')
   
    
    try:
        user_choice = clean_input(input('Choose your mode: REPL, FILE, OR TEXT EDITOR  '))
        if user_choice == 'REPL' or user_choice == 'CONSOLE':
            while True:
                try:
                    command = receive_expression()
                    command = clean_input(command)
                    if command == '%FINISH':
                        break
                    final_result = simplify_layers(command)
                    if final_result is not None:
                        print(final_result)
                    lines_of_code.append(command)
                except KeyboardInterrupt:
                    print()
                    print('Program has stopped unexpectedly... Going back to the command line..')
            export_wrapper(lines_of_code)
        elif user_choice == 'TEXT' or user_choice == 'TEXT EDITOR' or user_choice == 'EDITOR':
            # implement text editor mode here
            index = 1
            while True:
                print(f'{index}. ', end=' ')
                line = clean_input(input())
                if line == '%FINISH' or line == '%EXIT':
                    break
                lines_of_code.append(line)
                index += 1
            run_a_list_of_code(lines_of_code)
            export_wrapper()
            pass
        elif user_choice == 'FILE' or user_choice == 'IMPORT':
            # implement file import mode here
            name = input("File's name and/or path:  ")
            if not os.path.isfile(name):
                print(f"{name} does not exists in the specified context")
            else:
                with open(name, 'rt') as file:
                    for line in file:  # adding each line as an item in the list of code
                        lines_of_code.append(line)
                    run_a_list_of_code(lines_of_code)
    except KeyboardInterrupt as kb:
        print(' \n EXECUTION HAS BEEN CLOSED BY THE USER')


if __name__ == '__main__':
    main()