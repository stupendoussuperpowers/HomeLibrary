import pickle
from random import randrange
import os

class Library:
    def __init__(self,LibraryDatabase, MembershipID):
        try:
            self.LibraryDatabase = LibraryDatabase
            self.MembershipID = MembershipID
            f = open(LibraryDatabase,'rb')
            g = open(MembershipID,'rb')
            Library.database = pickle.load(f)
            Library.memid = pickle.load(g)
            f.close()
            g.close()
        except:
            print('Couldn\'t find an existing Library and/or Database. Creating an empty file instead.')
            Library.database = {}
            Library.memid = {}
            f = open(LibraryDatabase,'wb')
            g = open(MembershipID,'wb')
            f.close()
            g.close()
        print self.__str__()

    def display(self):
        print('--------------------------------------------------------------------------------------')
        print('NAME                               AUTHOR                GENRE               ISSUED BY')
        print('--------------------------------------------------------------------------------------')
        for i in Library.database.keys():
            print('%-30s   %-20s    %-18s   %7s'%(i,Library.database[i][0],Library.database[i][1],Library.database[i][2]))
        print('--------------------------------------------------------------------------------------')

    def issuingbook(self,issuebook):
        if issuebook in Library.database.keys():
            if Library.database[issuebook][-1] == 'None':
                while True:
                    try:
                        self.p = input('Enter your Membership ID: ')
                        break
                    except:
                        print("Error in parsing info enter again please")
                if self.p in Library.memid.keys():
                    if Library.memid[self.p] == 'None':
                        Library.database[issuebook][-1] = self.p
                        Library.memid[self.p] = issuebook
                        print('The book has been successfully issued!')
                    else:
                        print('Please return the issued book first!')
                else:
                    print('Member has not been registered yet!')

            else:
                print('The book has been currently issued to',Library.database[issuebook][-1])
        else:
            print('The book is not currently not available!')
        self.__update()

    def returningbook(self,mem):
        if mem in Library.memid.keys():
            if Library.memid[mem] != 'None':
                Library.database[Library.memid[mem]][-1] = 'None'
                Library.memid[mem] = 'None'
                print 'Book returned successfully'
            else:
                print 'No book has been issued to this Membership ID' 
        else:
            print('The Membership ID is not registered yet!')
        self.__update()

    
    def __update(self):
        
        f = open('Library1.txt','wb')
        g = open('MemID1.txt','wb')
        pickle.dump(Library.database,f)
        pickle.dump(Library.memid,g)
        f.close()
        g.close()
        os.remove(self.LibraryDatabase)
        os.rename('Library1.txt', self.LibraryDatabase)
        os.remove(self.MembershipID)
        os.rename('MemID1.txt', self.MembershipID)


    def newbook(self,newname,newauthor,genre):
        if len(newname) > 30:
            newname = newname[0:30]
        if newname in Library.database:
            print('The Book already exists')
            print('----> %s, by %s'%(newname,Library.database[newname][0]))
            
        if len(newauthor) > 20:
            newauthor = newauthor[0:20]
        if len(genre) > 18:
            genre = genre[0:20]
            
        Library.database[newname] = [newauthor,genre,'None']
        self.__update()

    def addmem(self):
        while True:
            self.newID = randrange(9999)
            if self.newID not in Library.memid.keys():
                print('New Membership number is %d'%self.newID)
                break
        Library.memid[self.newID] = 'None'
        self.__update()

    def memberlist(self):
        print('-'*86)
        print('Membership ID           Book Issued')
        print('-'*86)
        for i in Library.memid.keys():
            print('%-15s    %15s'%(i,Library.memid[i]))

    def changebook(self):
        print('Select the parameter to Edit:')
        print('1. Name of the Book')
        print('2. Author of the Book')
        choice = raw_input()
        if choice == '1':
            self.oldname = raw_input('Enter the current name of the book:')
            try:
                f = Library.database[self.oldname]
                self.newname = raw_input('Enter new name:')
                Library.database[self.newname] = [f[0],f[1],f[2]]
                del Library.database[self.oldname]
            except:
                print('Book does not exist in the database!')
            
        elif choice == '2':
            self.bname = raw_input('Enter name of the Book:')
            try:
                f = Library.database[self.bname]
                Library.database[bname][0] = raw_input('Enter new name of the Author:')
            except:
                print('Book does not exist in the database!')

        self.__update()

    def removebook(self,bremove):
        try:
            del Library.database[bremove]
        except:
            print('The book was not here anyways!')
        self.__update()

    def removeMem(self,mremove):
        if Library.memid[mremove] != 'None':
            while True:
                print('Looks like the member still has a book, Return the book first! Enter Details below:')
                memid = input('Enter your Membership ID: ')
                if memid in Library.memid.keys():
                    self.returningbook(memid)
                    break

        del Library.memid[mremove]

    def viewbyAuthor(self,authorname):
        print('--------------------------------------------------------------------------------------')
        print('NAME                               AUTHOR                GENRE               ISSUED BY')
        print('--------------------------------------------------------------------------------------')
        for i in Library.database.keys():
            if Library.database[i][0] == authorname:
                print('%-30s   %-20s    %-18s   %7s'%(i,Library.database[i][0],Library.database[i][1],Library.database[i][2]))
        print('----------------------------------------------------------------')
        bname = raw_input('Enter the name of the book to issue. Press "N" to exit: ')
        if bname in Library.database.keys():
            self.issuingbook(bname)
        elif bname.lower() == 'n':
            pass
        else:
            print('Book doesn\'t exist in the Library Database')

    def viewbyName(self,searchname):
        if searchname in Library.database.keys():
            print('--------------------------------------------------------------------------------------')
            print('NAME                               AUTHOR                GENRE               ISSUED BY')
            print('--------------------------------------------------------------------------------------')
            print('%-30s   %-20s    %-18s   %7s'%(searchname,Library.database[searchname][0],Library.database[searchname][1],Library.database[searchname][2]))
            print('--------------------------------------------------------------------------------------')
            choice = raw_input('Do you wish to issue this book? Y: Yes N: No')
            if choice.lower() == 'y':
                self.issuingbook(searchname)
        else:
            print 'Couldn\'t find the book in the database, did you mean any of the following? - '
            print('--------------------------------------------------------------------------------------')
            print('NAME                               AUTHOR                GENRE               ISSUED BY')
            for i in Library.database.keys():
                if self.__patternsearch(searchname,i):
                    print('--------------------------------------------------------------------------------------')
                    print('%-30s   %-20s    %-18s   %7s'%(i,Library.database[i][0],Library.database[i][1],Library.database[i][2]))
            print('--------------------------------------------------------------------------------------')
        bname = raw_input('Enter the name of the book you want to issue, press "N" to Quit:')
        if bname.lower() == 'n':
            pass
        else:
            self.viewbyName(bname)

        
    def viewbyGenre(self,genre):
        print('--------------------------------------------------------------------------------------')
        print('NAME                               AUTHOR                GENRE               ISSUED BY')
        print('--------------------------------------------------------------------------------------')
        for i in Library.database.keys():
            if Library.database[i][-2].lower() == genre.lower():
                print('%-30s   %-20s    %-18s   %7s'%(i,Library.database[i][0],Library.database[i][1],Library.database[i][2]))
        print('--------------------------------------------------------------------------------------')

    def __str__(self):
        print('DATABASE DETAILS'.center(86,'-'))
        return ' Library Book Database: %s \n Membership Database: %s \n Total Number of Books: %d \n Total Number of Members: %d '%(self.LibraryDatabase, self.MembershipID,len(Library.database),len(Library.memid))

    def __del__(self):
        return '''Deleting the Library and Membership Database'''

class FrontEnd(Library):
    def __init__(self,LibraryDatabase,MembershipID):
        self.LibraryDatabase = LibraryDatabase
        self.MembershipID = MembershipID
        Library.__init__(self,self.LibraryDatabase, MembershipID)
        pause = raw_input('Press Enter to Continue')
        os.system('cls')
        while True:
            try:
                print('MAIN MENU'.center(86,'-'))
                print('1.  Book List')
                print('2.  Check Members')
                print('3.  Issue a Book')
                print('4.  Return a Book')
                print('5.  Add a New Book')
                print('6.  Add a New Member')
                print('7.  Edit a Book')
                print('8.  Remove a Book')
                print('9.  Remove a Member')
                print('10. View Books from a Author')
                print('11. View Books by genre')
                print('12. Search Book by Name')
                print('13. Quit the Program')
                choice = int(raw_input())
                os.system('cls')
                if choice not in [i for i in range(1,14)]:
                    print('Please enter a valid choice!')
                    continue
                if choice == 1:
                    print('BOOK LIST'.center(86,'-'))
                    self.display()
                elif choice == 2:
                    print('MEMBER LIST'.center(86,'-'))
                    self.memberlist()
                    
                elif choice == 3:
                    print('ISSUE A BOOK'.center(86,'-'))
                    issuebook = raw_input('Enter the book you want to issue:')
                    self.issuingbook(issuebook)

                elif choice == 4:
                    print('RETURN A BOOK'.center(86,'-'))
                    mem = input('Enter your Membership ID:')
                    self.returningbook(mem)

                elif choice == 5:
                    print('ADD A NEW BOOK'.center(86,'-'))
                    newbook = raw_input('Enter the name of the book: ')
                    author = raw_input('Enter the name of the author: ')
                    genre = raw_input('Enter the genre of the book: ')
                    self.newbook(newbook,author,genre)

                elif choice == 6:
                    print('ADD A NEW MEMBER'.center(86,'-'))
                    self.addmem()

                elif choice == 7:
                    print('EDIT A BOOK'.center(86,'-'))
                    self.changebook()

                elif choice == 8:
                    print('REMOVE A BOOK'.center(86,'-'))
                    bremove = raw_input('Enter the name of the book: ')
                    self.removebook(bremove)

                elif choice == 9:
                    print('REMOVE A MEMBER'.center(86,'-'))
                    mremove = input('Enter the Membership ID: ')
                    self.removeMem(mremove)

                elif choice == 10:
                    print('BOOKS BY A AUTHOR'.center(86,'-'))
                    author = raw_input('Enter the name of the author: ')
                    self.viewbyAuthor(author)

                elif choice == 11:
                    genre = raw_input('Enter the genre:')
                    self.viewbyGenre(genre)

                elif choice == 12:
                    print('BOOK SEARCH'.center(86,'-'))
                    bsearch = raw_input('Enter the name of the book: ')
                    self.viewbyName(bsearch)

                elif choice == 13:
                    print('Exiting the Program')
                    self.__del__()
                    break
                pause = raw_input('Press any key to continue:')
                os.system('cls')
            except ValueError:
                print 'Invalid Input'
                continue

b = FrontEnd('Library.txt','MemID.txt')
