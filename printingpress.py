import io
import sys 
import pyperclip

def format_string(str):#makes the text formatting acceptable for a command, returns a string
    str = str.strip('\n') #remove stray newlines
    str = str.replace('\\', '\\\\\\\\') #escape esacpes 
    str = str.replace('\'', '\\\'') #escape single quotes 
    str = str.replace('"', '\\\\"') # escape double quotes
    return str

def atlas(page): #specific case for my own book, returns a string to mark a page as a clickable event 
        at= page.find('@') #python sucks
        if(at == -1): #skip pages without it
            spec_page= '\"}\',' #regular page end
            return spec_page
        location= page[at+2:page.find('\n', at)].replace(',','') #the loctions that /tp accepts are 3 numbers separated by a space
        spec_page= '\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\" /tp '+location #run command syntax
        spec_page+= '\"}}\',' #special page end, still ends with a comma so no extra action needs to be taken
        return spec_page

TEST = False
#arg 1 is the text file containing the book's pages
book_src = open(sys.argv[1],'r')

generation = -1

print('Title: ')
book_title = input()
print('Author: ')
book_author = input() 

while(generation > 3 or generation <= 0):
    print('Generation: \t\n\t0) Original \n\t1) Copy of Original \n\t2) Copy of Copy \n\t3) Tattered')
    generation = int(input())

#command prefix, this is what all give commands start with 
command_out = '/give @p written_book{pages:['

try:
    page_list = book_src.read().split('//') #valid book files mark the end of a page with //
except IOError:
    print("File Error") 

# page_list[:-1] because it tends to read in an extra blank page
for page in page_list[:-1]:
    #page format is '{"text":"Page Text"}',
    command_out += '\'{\"text\":\"'
    command_out += format_string(page) #for escapes and quotes and stuff that messes with the command
    if(sys.argv[1]=='new_atlas.txt'): #for a specific book
        command_out+= atlas(page)
    else:
        command_out+= '\"}\',' #a regular single page ends with this
    if(TEST): #console testing
        print(page) 

#remove the comma from the end of the page list and preserve new lines
command_out = command_out[:-1].replace('\n','\\\\n')

#command suffix, generation:1 means the book will be marked as copy of original
command_out += '],title:\"'+book_title+'\",author:\"'+book_author+'\",generation:'+str(generation)+'}'

pyperclip.copy(command_out)
print('Command copied to clipboard!')


