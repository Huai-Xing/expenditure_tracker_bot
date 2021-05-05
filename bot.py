import datetime
import db
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

#For heruko
import os
PORT = int(os.environ.get('PORT', 5000))

#For logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#Default parameters for Bot
currentuser = 0
callbacktype = "1" 
catetype = 10
category = ["Budget","Food", "Transport", "Bills", "Shopping", "Fun", "Gifts", "Others"] #Categories for spending
resetnum = 10
resetType = ["current month", "current year", "entire bot"]
now = datetime.datetime.now()
callyear = now.year
budgetset = False

#Checks if there is a need to create a new document for the database
def checkData():
    global currentuser
    global budgetset
    now = datetime.datetime.now()
    later = now + datetime.timedelta(hours=12)
    curryear = now.year
    currmonth = now.month - 1
    if later.month != now.month:
        currmonth = later.month - 1
    if not db.check_data(curryear, currmonth, 0, currentuser):
        db.create_new_year(curryear, currentuser)
    if not db.check_data(curryear, currmonth, 1, currentuser):
        db.create_new_month(curryear, currmonth, currentuser)
        budgetset = True

#Command to initialise the bot. Send users inline keyboard options.
def start(update, context):
    global currentuser
    #Checks for user to determine which database to read and write data to
    if update.message.chat.username == id1 or update.message.chat.username == id2:
        if update.message.chat.username == id1:
            currentuser = 0
        else: 
            currentuser = 1
        checkData()
        global callbacktype
        global catetype
        global budgetset
        budgettext = ""
        if budgetset:
            budgettext = "\n\n<u>Please set budget for the new month.</u>"
        callbacktype = "1"
        catetype = 10
        keyboard = [[InlineKeyboardButton("Current month status", callback_data='1')],
            [InlineKeyboardButton("Add budget", callback_data='2')],
            [InlineKeyboardButton("Add spending", callback_data='3')],
            [InlineKeyboardButton("See previous data", callback_data='4')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "<b>Welcome to Saving So Baby Can Be A Tai Tai</b>!\n\nTo begin, please select an action." + budgettext, parse_mode='HTML', reply_markup=reply_markup)
        budgetset = False

#Command to view all available bot actions        
def actions(update, context):
    global currentuser
    #Checks for user to determine which database to read and write data to
    if update.message.chat.username == id1 or update.message.chat.username == id2:
        if update.message.chat.username == id1:
            currentuser = 0
        else: 
            currentuser = 1
        checkData()
        global callbacktype
        global catetype
        global budgetset
        budgettext = ""
        if budgetset:
            budgettext = "\n\n<u>Reminder to set budget for the new month.</u>"
        callbacktype = "1"
        catetype = 10
        keyboard = [[InlineKeyboardButton("Current month status", callback_data='1')],
            [InlineKeyboardButton("Add budget", callback_data='2')],
            [InlineKeyboardButton("Add spending", callback_data='3')],
            [InlineKeyboardButton("See previous data", callback_data='4')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "What would you like to do now?" + budgettext, parse_mode='HTML', reply_markup=reply_markup)
        budgetset = False

#Command to add spending for current month
def add(update, context):
    global currentuser
    #Checks for user to determine which database to read and write data to
    if update.message.chat.username == id1 or update.message.chat.username == id2:
        if update.message.chat.username == id1:
            currentuser = 0
        else: 
            currentuser = 1
        checkData()
        global callbacktype
        global catetype
        global budgetset
        budgettext = ""
        if budgetset:
            budgettext = "<u>Reminder to set budget for the new month.</u>\n\n"
        keyboard = [[InlineKeyboardButton("Food", callback_data='1'), InlineKeyboardButton("Transport", callback_data='2')],
            [InlineKeyboardButton("Bills", callback_data='3'), InlineKeyboardButton("Shopping", callback_data='4')],
            [InlineKeyboardButton("Fun", callback_data='5'), InlineKeyboardButton("Gifts", callback_data='6')],
            [InlineKeyboardButton("Others", callback_data='7')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            budgettext + "Please select spending category:", parse_mode='HTML', reply_markup=reply_markup)
        callbacktype = "2"
        budgetset = False

#Command to reset user data by month or year     
def reset(update, context):
    global currentuser
    #Checks for user to determine which database to read and write data to
    if update.message.chat.username == id1 or update.message.chat.username == id2:
        if update.message.chat.username == id1:
            currentuser = 0
        else: 
            currentuser = 1
        checkData()
        global callbacktype
        keyboard = [[InlineKeyboardButton("Reset current month to 0", callback_data='0')],
            [InlineKeyboardButton("Reset current year to 0", callback_data='1')],
            [InlineKeyboardButton("Reset entire bot", callback_data='2')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "What would you like to reset?", parse_mode='HTML', reply_markup=reply_markup)
        callbacktype = "4"

#Command to view paired user data        
def peek(update, context):
    global currentuser
    #Checks for user to determine which database to read and write data to
    if update.message.chat.username == id1 or update.message.chat.username == id2:
        if update.message.chat.username == id1:
            currentuser = 0
        else: 
            currentuser = 1
        checkData()
        global callbacktype
        keyboard = [[InlineKeyboardButton("Peek at baby current month status", callback_data='0')],
            [InlineKeyboardButton("Peek at baby full month overview", callback_data='1')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "What would you like to peek?", parse_mode='HTML', reply_markup=reply_markup)
        callbacktype = "6"

#callback data responds        
def button(update, context):
    checkData()
    global callbacktype
    global catetype
    global currentuser
    global category
    global resetType
    global resetnum
    global callyear
    query = update.callback_query
    query.answer()
    
    #First call back from user - from main menu
    if callbacktype == "1":
        #Data call back 1 - Get current month data
        if query.data[0] == "1":
            text = GetCurrentMonth(currentuser)
            query.edit_message_text(text, parse_mode='HTML')
        #Data call back 2 - Set current month budget
        elif query.data[0] == "2":
            text = "Please send in your budget"
            query.edit_message_text(text, parse_mode='HTML')
            catetype = 0
        #Data call back 3 - Add current month spending
        elif query.data[0] == "3":
            text = "Please select spending category:"
            keyboard = [[InlineKeyboardButton("Food", callback_data='1'), InlineKeyboardButton("Transport", callback_data='2')],
                [InlineKeyboardButton("Bills", callback_data='3'), InlineKeyboardButton("Shopping", callback_data='4')],
                [InlineKeyboardButton("Fun", callback_data='5'), InlineKeyboardButton("Gifts", callback_data='6')],
                [InlineKeyboardButton("Others", callback_data='7')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)
            callbacktype = "2"
        #Data call back 4 - View historical data
        else:
            text = "Please input year"
            query.edit_message_text(text, parse_mode='HTML')
            callbacktype = "3"
    #Second call back from user - from spending menu
    elif callbacktype == "2":
        text = "Please send in amount spent for "
        catetype = int(query.data[0])
        query.edit_message_text(text + category[catetype], parse_mode='HTML')
    #Fourth call back from user - from reset button
    elif callbacktype == "4":
        resetnum = int(query.data)
        text = "Are you sure you want to reset {x}? This action cannot be undone!".format(x = resetType[resetnum])
        keyboard = [[InlineKeyboardButton("Yes", callback_data='1')],
            [InlineKeyboardButton("No", callback_data='2')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)
        callbacktype = "5"
    #Fifth call back from user - from reset menu
    elif callbacktype == "5":
        ans = int(query.data)
        now = datetime.datetime.now()
        curryear = now.year
        currmonth = now.month - 1
        if ans == 1:
            text = "The {x} has been resetted".format(x = resetType[resetnum])
            if resetnum == 0:
                db.reset_month(curryear, currmonth, currentuser)
            elif resetnum == 1:
                db.reset_year(curryear, currentuser)
            else:
                db.reset_collection(currentuser)
        else:
            text = "Reset aborted."
        query.edit_message_text(text, parse_mode='HTML')
        resetnum = 3
        callbacktype = "0"
    #Sixth call back from user - from peek button
    elif callbacktype == "6":
        user = 0
        if currentuser == 0:
            user = 1
        if query.data[0] == "0":
            text = GetCurrentMonth(user)
            query.edit_message_text(text, parse_mode='HTML')
        else:    
            now = datetime.datetime.now()
            curryear = now.year    
            text = GetData(curryear, 13, user)
            query.edit_message_text(text, parse_mode='HTML')
        callbacktype = "0"
    #Invalid call back from user - return default call back
    else:
        text = GetData(callyear, int(query.data), currentuser)
        query.edit_message_text(text, parse_mode='HTML')
        callbacktype = "0"

#Read in text input from user and to respond accordingly        
def text(update, context):
    global currentuser
    #Checks for user to determine which database to read and write data to
    if update.message.chat.username == id1 or update.message.chat.username == id2:
        if update.message.chat.username == id1:
            currentuser = 0
        else: 
            currentuser = 1
        checkData()
        global callbacktype
        global category
        global catetype
        global callyear
        currnow = datetime.datetime.now()
        curryear = currnow.year
        currmonth = currnow.month - 1
        value = update.message.text
        #Update budget
        if callbacktype == "1" and catetype == 0:
            data = db.update(curryear, currmonth, catetype, float(value), currentuser)
            db.update(curryear, 12, catetype, float(value), currentuser)
            update.message.reply_text("Budget is now updated to $" + value, parse_mode='HTML')
            callbacktype = "0"
        #Update spending
        elif callbacktype == "2":
            data = db.update(curryear, currmonth, catetype, float(value), currentuser)
            db.update(curryear, 12, catetype, float(value), currentuser)
            old = "{O:.2f}".format(O = data[1])
            new = "{N:.2f}".format(N = data[2])
            update.message.reply_text(category[catetype] + " is updated from $" + old + " to $" + new, parse_mode='HTML')
            callbacktype = "0"
        #View historical data
        elif callbacktype == "3":
            #Invalid date
            if not db.check_data(int(value), 0, 0, currentuser)and int(value) > 2020:
                text = " is in the future and there is no data yet. \nPlease enter another year, or type '/actions' to see available actions."
                update.message.reply_text(str(value) + text, parse_mode='HTML')              
            elif int(value) < 2021:
                text = " is not a valid year. \n(Hint: Year has to be 2021 onwards) \nPlease enter the year again, or type '/actions' to see available actions."
                update.message.reply_text(str(value) + text, parse_mode='HTML')
            else:
                callyear = value
                text = "Please select month:"
                keyboard = [[InlineKeyboardButton("Full Year Overview", callback_data='12')],
                    [InlineKeyboardButton("Monthly Overview", callback_data='13')],
                    [InlineKeyboardButton("Jan", callback_data='0'), InlineKeyboardButton("Feb", callback_data='1')],
                    [InlineKeyboardButton("Mar", callback_data='2'), InlineKeyboardButton("Apr", callback_data='3')],
                    [InlineKeyboardButton("May", callback_data='4'), InlineKeyboardButton("Jun", callback_data='5')],
                    [InlineKeyboardButton("Jul", callback_data='6'), InlineKeyboardButton("Aug", callback_data='7')],
                    [InlineKeyboardButton("Sep", callback_data='8'), InlineKeyboardButton("Oct", callback_data='9')],
                    [InlineKeyboardButton("Nov", callback_data='10'), InlineKeyboardButton("Dec", callback_data='11')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(text, parse_mode='HTML', reply_markup=reply_markup)              
        #View available actions
        else:
            keyboard = [[InlineKeyboardButton("Current month status", callback_data='1')],
                [InlineKeyboardButton("Add budget", callback_data='2')],
                [InlineKeyboardButton("Add spending", callback_data='3')],
                [InlineKeyboardButton("See previous data", callback_data='4')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                "Please select an action:", parse_mode='HTML', reply_markup=reply_markup)
            callbacktype = "1"

token = '<Token for telegram bot>'
id1 = '<Id of restricted user>'
id2 = '<Id of restricted user>'

#Retrieve and format all month data for the entire year for user
def GetAllData(yearNum, monthCat, user):
    data = db.find(yearNum, 12, user)
    amtspent = data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7]
    amtsaved = data[0] - data[1] - data[2] - data[3] - data[4] - data[5] - data[6] - data[7]
    pos = ""
    if amtsaved < 0:
        pos = "-"
    amtsaved = abs(amtsaved)
    fulloutput = "<b><u>Full status for {y}: </u></b>\
        \n<b>Budget: ${T1:.2f} </b>\
        \n<b>Total amount spent: ${T2:.2f} </b>\
        \n<b>Total amount saved: {P}${T3:.2f} </b>\
        \n".format(y = yearNum, T1 = data[0], T2 = amtspent, T3 = amtsaved, P = pos)
    for x in range(12):
        if not db.check_data(yearNum, x, 1, user):
            curroutput = "\n\n<u>{M}: </u>\
                No data available".format(M = monthCat[x])
        else:
            data = db.find(yearNum, x, user)
            amtspent = data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7]
            amtsaved = data[0] - data[1] - data[2] - data[3] - data[4] - data[5] - data[6] - data[7]
            pos = ""
            if amtsaved < 0:
                pos = "-"
            amtsaved = abs(amtsaved)
            curroutput = "\n\n<u>{M}: </u>\
                \n<b>Budget: ${L1:.2f} </b>\
                \n<b><i>Amount spent: ${L9:.2f} </i></b>\
                \n<b><i>Amount saved: {P}${L10:.2f} </i></b>\
                \nFood: ${L2:.2f} \
                \nTransport: ${L3:.2f} \
                \nBills: ${L4:.2f} \
                \nShopping: ${L5:.2f} \
                \nFun: ${L6:.2f} \
                \nGifts: ${L7:.2f} \
                \nOthers: ${L8:.2f}".format(M = monthCat[x], L1 = data[0], L2 = data[1], L3 = data[2], L4 = data[3], L5 = data[4], L6 = data[5], L7 = data[6], L8 = data[7], L9 = amtspent, L10 = amtsaved, P = pos)
        fulloutput += curroutput
    return fulloutput

#Retrieve and format specific month data for user
def GetData(yearNum, month, user):
    yearNum = int(yearNum)
    month = int(month)
    monthCat = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "whole of"]
    output = "<b><u>Status for {m} {y}: </u></b>\
        \n<b>Budget: ${L1:.2f} </b>\
        \nFood: ${L2:.2f} \
        \nTransport: ${L3:.2f} \
        \nBills: ${L4:.2f} \
        \nShopping: ${L5:.2f} \
        \nFun: ${L6:.2f} \
        \nGifts: ${L7:.2f} \
        \nOthers: ${L8:.2f} \
        \n\nAmount spent: ${L9:.2f} \
        \nAmount saved: {P}${L10:.2f}"
    if month == 13:
        return GetAllData(yearNum, monthCat, user)
    elif not db.check_data(yearNum, month, 1, user):
        return "There is no data for " + str(monthCat[month]) + " " + str(yearNum)
    else:
        data = db.find(yearNum, month, user)
        amtspent = data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7]
        amtsaved = data[0] - data[1] - data[2] - data[3] - data[4] - data[5] - data[6] - data[7]
        pos = ""
        if amtsaved < 0:
            pos = "-"
        amtsaved = abs(amtsaved)
        return output.format(m = monthCat[month], y = yearNum, L1 = data[0], L2 = data[1], L3 = data[2], L4 = data[3], L5 = data[4], L6 = data[5], L7 = data[6], L8 = data[7], L9 = amtspent, L10 = amtsaved, P = pos)

#Retrieve and format current month data for user
def GetCurrentMonth(user):
    currnow = datetime.datetime.now()
    curryear = currnow.year
    currmonth = currnow.month - 1
    data = db.find(curryear, currmonth, user)
    endmonth = datetime.date(curryear,currmonth + 2,1) - datetime.timedelta(days=1)
    diffdays =  (endmonth - datetime.date.today()).days
    amtspent = data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7]
    amtsaved = data[0] - data[1] - data[2] - data[3] - data[4] - data[5] - data[6] - data[7]
    amtleftperday = amtsaved / diffdays
    pos = ""
    over = ""
    if amtsaved < 0:
        pos = "-"
        amtleftperday = 0
        over = "\n\nOVERSPEND!!!!"
    amtsaved = abs(amtsaved)
    output = "<b><u>Current month status: </u></b>\
        \n<b>Budget: ${L1:.2f} </b>\
        \nFood: ${L2:.2f} \
        \nTransport: ${L3:.2f} \
        \nBills: ${L4:.2f} \
        \nShopping: ${L5:.2f} \
        \nFun: ${L6:.2f} \
        \nGifts: ${L7:.2f} \
        \nOthers: ${L8:.2f} \
        <b><u>{over}</u></b> \
        \n\nAmount spent: ${L9:.2f} \
        \nAmount saved: {P}${L10:.2f} \
        \n\nDays left to end of month: <b><u>{D}</u></b> \
        \nAmount left to spend per day: <b><u>${A:.2f}</u></b>"
    return output.format(L1 = data[0], L2 = data[1], L3 = data[2], L4 = data[3], L5 = data[4], L6 = data[5], L7 = data[6], L8 = data[7], L9 = amtspent, L10 = amtsaved, P = pos, D = diffdays, A = amtleftperday, over = over)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher
    
    #Telegram bot commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("actions", actions))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("peek", peek))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text))
    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_error_handler(error)
    
    #For heruko instead of update.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=token)
    updater.bot.setWebhook('https://<appname>.herokuapp.com/' + token)
    
    # updater.start_polling()
    

    updater.idle()



if __name__ == '__main__':
    main()
