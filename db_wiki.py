
# 1st - Feb - 2022
#=================

#Author: P. A. Ogbodum
#=====================

#Program Description: A dictionary app that queries a remote database and return the meaning of a word entered by a user
#====================

#Program Name: db_wiki v1
#========================

# Future update: Add a UI that collects database login credentials to aid smooth db connection and prevent messing with code all the time.

def db_wiki():
    
    import mysql.connector as mc
    from difflib import get_close_matches as cm
    
    #establish connection, if there was a password, then you would include a password paramter for the .connect method
    conn = mc.connect(
    user='root',
    host='127.0.0.1',
    database='dictapp')
    
    #next we create a cursor instance/object which will allow us to execute sql queries.
    cur = conn.cursor()

    #next we begin to execute queries with the .execute() method of the cursor method
    query = cur.execute('SELECT word FROM dictionary')

    #to return/fetch all the results of the previous query from the database, we use the .fetchall() method of the .cursor method
    query_result=cur.fetchall()
    
    #convert the words from list of tuples to list of strings
    word_list = ['%s' %i for i in query_result]
    
    # 1. receive user input
    user_word = input('Enter word: ')
    #convert the user entered word to lowercase
    user_word = str(user_word).lower()
    
    # 2. check if the user have enterd a valid word/if the variable contains a word
    if user_word:
        
        # 3. check if user word is contained in the list of words in the dictionary
        if user_word in word_list:
            print(f'{user_word} \n')
            #get word meaning from the dictionary
            defs_1 = cur.execute(f'SELECT meaning FROM dictionary WHERE word = "{user_word}" ') #you can change word to whatever name the word column is designated with
            #return results for query k_words and coverts it from list of tuples to list of strings
            qry_1 = cur.fetchall()
            out1 = ['%s' %i for i in qry_1]
            #remove the quotes, commas and brackets from the list strings
            print(', '.join(out1))
            
        # 4. check for similar/words closely matching that of the user's for mis-spelt words
        elif len(cm(user_word, word_list, n=5, cutoff=0.65)) > 0:
            #get list of words closely matching that of the user
            word_guessed = cm(user_word, word_list, n=5, cutoff=0.65)
            #remove the quotes, commas and brackets from the list strings
            word_guessed = ', '.join(word_guessed)
            #ask the user to confirm result of returned suggested word
            re_check = input(f'Did you mean any of the following word(s): {word_guessed} ? If yes type Y,\
if no, N: ')
            re_check = re_check.upper()
            if re_check == 'Y':
                user_word = input('Enter word: ')
                user_word = str(user_word).lower()
                elif_word = cur.execute(f'SELECT meaning FROM dictionary WHERE word = "{user_word}" ')
                result_b = ['%s' %i for i in cur.fetchall()]
                print(f'{user_word} \n')
                print(', '.join(result_b))
            elif re_check == 'N':
                print('  End of program')
            else:
                print('  Sorry, the word you entered doesn\'t exist in this dictionary. Double check and try again')
        
        # 5. if the word was not mis-spelt or contained in the dictionary
        else:
            print('  Sorry, the word you entered doesn\'t exist in this dictionary. Double check and try again')
    
    # 6. if the user did not enter a word/valid word
    else:
        print('  Sorry, the word you entered doesn\'t exist in this dictionary. Double check and try again')