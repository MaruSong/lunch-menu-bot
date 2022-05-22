`lunch-menu-bot` is a bot sending the daily lunch menu to the Alavi department's zulip chat.
### Hot it works
Every day at a given time, `main.py` is executed by `cron`. `main.py` first checks if today's menu file exists in `menu_data/`. 
If the file exists, `send_message` function is executed to send the menu of the day to the zulip chat. 
If not, `request` and `parser` functions are executed in order. Then the code checks again if today's menu file exists and 
send the menu to the zulipchat if the menu file is found. 
##### `request.py`
`request` function sends MPI-FKF intranet a request to download the latest lunch menu pdf file.
Valid `cookie.dat` should be prepared before executing `request` function. 
A successful request saves `menu.pdf` in `menu_data/`.
##### `parser.py`
`parser` function uses `pdfminer` library. The function parses the menu pdf, gather texts, and classify them based on given coordinates.
This means the coordinates should be changed if the layout of the menu pdf file is changed. Each day's menu is saved in `pickle` format
in `menu_data/`. The filename of a `.pickle` file indicates the timestamp of the day when the menu is served.
##### `send_message.py`
`send_message` function uses `zulip` python library. With the prepared `zuliprc` file, the function sends the menu of the day to
the zulip chat.

### Planned features
1. Automating `request` part.
 - Until the implementation of the feature, I have to update `cookie.dat` regularly.
1. Sending weekly menu once a week.
 - Currently, `lunch-menu-bot` send the lunch menu of the day to zulip every morning. 
 Sending a weekly menu once a week looks better, as the code would be simpler and people can find the weekly menu at once.
 - Or, this feature can be substitutied by enabling interactive-bot function (not sure if it is supported by zulip bots). 
 Then a zulip user type something in the chat so that `lunch-menu-bot` prints the weekly menu.
