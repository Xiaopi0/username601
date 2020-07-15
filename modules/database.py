from pymongo import MongoClient
import os
from sys import path
from datetime import datetime as t
from random import choice
import requests
path.append('/app/modules')
from username601 import *

database = MongoClient(os.environ['DB_LINK'])['username601']

class WelcomeGoodbye:
    def add(guildid, channelid):
        database["config"].update_one({"type": "wlcm"}, { "$push": {"wlcm": str(guildid)+"|"+str(channelid)} })
    def guild_quit(guildid):
        data = database["config"].find({"type": "wlcm"})[0]["wlcm"]
        found = [str(i) for each in range(0, len(data)) if data[each].startswith(str(guildid))]
        if len(found)==0: return False
        database["config"].update_one({"type": "wlcm"}, { "$pull": {"wlcm": found[0]}})
        return True
    def channel_quit(channelid):
        data = database["config"].find({"type": "wlcm"})[0]["wlcm"]
        found = [str(i) for each in range(0, len(data)) if data[each].endswith(str(channelid))]
        if len(found)==0: return False
        database["config"].update_one({"type": "wlcm"}, { "$pull": {"wlcm": found[0]}})
        return True
    def get_logging_channel(guildid):
        return int([i for i in range(0, len(database["config"].find({"type": "wlcm"})[0]["wlcm"])) if i.startswith(str(guildid))][0].split('|')[1])
    def is_exist(guildid):
        if len([i for i in range(0, len(database["config"].find({"type": "wlcm"})[0]["wlcm"])) if i.startswith(str(guildid))])==0: return False
        return True
    def move(guildid, newchannelid):
        index = None
        for each in range(0, len(database["config"].find({"type": "wlcm"})[0])):
            if each.startswith(str(guildid)):
                index = i ; break
        if index==None: return False
        index = "wlcm.{}.value".format(str(index))
        database["config"].update_one({"type": "wlcm"}, {"$set": {index: str(guildid)+"|"+str(newchannelid)}})
        return True

class Economy:
    def get(userid):
        try:
            data = database["economy"].find({"userid": userid})[0]
            return data
        except Exception as e:
            return None
    def leaderboard(guildMembers):
        fetched, total = database["economy"].find(), []
        for i in fetched:
            if i["userid"] in [a.id for a in guildMembers]:
                total.append(str(i["userid"])+"|"+str(i["bal"]))
            else: continue
        return total
    
    def setdesc(userid, newdesc):
        try:
            database["economy"].update_one({"userid": userid}, { "$set": { "desc": str(newdesc) } })
        except:
            return 'error'
    def vote(userid, bl):
        try:
            database["economy"].update_one({"userid": userid}, { "$set": { "voted": bl } })
        except:
            return 'error'

    def can_vote(userid):
        data = requests.get("https://api.ksoft.si/webhook/dbl/check?bot={}&user={}".format(str(Config.id), str(userid)), headers={"authorization":"Bearer "+str(os.environ['KSOFT_TOKEN'])}).json()
        if not data['voted'] or Economy.get(userid)['voted']==False:
            return {
                "bool": True,
                "time": None
            }
        else:
            return {
                "bool": False,
                "time": data['data']['expiry'].split('T')[0]+' '+data['data']['expiry'].split('T')[1][:-7]
            }
    
    def setbal(userid, newbal):
        if userid not in [i["userid"] for i in database["economy"].find()]:
            return 'user has no profile'
        else:
            try:
                database["economy"].update_one({"userid": userid}, { "$set": { "bal": newbal } })
                return '200 OK'
            except Exception as e:
                return e

    def new(userid):
        try:
            database["economy"].insert_one({
                "userid": userid,
                "bal": 0,
                "desc": "nothing here!",
                "voted": False
            })
            return 'done'
        except Exception as e:
            return e
    def addbal(userid, bal):
        try:
            old = database["economy"].find({"userid": userid})
            database["economy"].update_one({"userid": userid}, { "$set": { "bal": old[0]['bal']+bal } })
            return 'success'
        except Exception as e:
            return e
    def delbal(userid, bal):
        try:
            old = database["economy"].find({"userid": userid})
            database["economy"].update_one({"userid": userid}, { "$set": { "bal": old[0]['bal']-bal } })
            return 'success'
        except Exception as e:
            return e
    
    def daily(userid):
        try:
            bal = choice([500, 1000, 1500, 2000, 2500, 3000])
            old = database["economy"].find_one({"userid": userid})
            database["economy"].update_one({"userid": userid}, { "$set": {
                "bal": old["bal"]+bal
            }})
            return bal
        except Exception as e:
            return e
    
    def changedesc(userid, newdesc):
        try:
            data = database["economy"].find({"userid": userid})
            if len(data)==0 or data==None:
                return 'undefined'
            else:
                database["economy"].update_one({"userid": userid}, { "$set": { "desc": str(newdesc) } })
                return 'success'
        except Exception as e:
            return 'e'

class selfDB:
    def post_uptime():
        for i in database["config"].find():
            if "uptime" in list(i.keys()):
                old_uptime = i["uptime"] ; break
        database["config"].update_one({"uptime": old_uptime}, { "$set": { "uptime": t.now().timestamp() } })
    def get_uptime():
        for i in database["config"].find():
            if "uptime" in list(i.keys()):
                uptime = i["uptime"] ; break
        time = str(t.now() - t.fromtimestamp(uptime))[:-7]
        return time+'|'+str(t.fromtimestamp(uptime))[:-7]
    def feedback_ban(userid, reason):
        for i in database["config"].find():
            if "bans" in list(i.keys()):
                old_bans = i["bans"] ; break
        database["config"].update_one({"bans": old_bans}, { "$push": {"bans": str(userid)+"|"+str(reason)} })
    def feedback_unban(userid):
        try:
            for i in database["config"].find():
                if "bans" in list(i.keys()):
                    for j in i["bans"]:
                        if j.startswith(str(userid)): reason = j.split('|')[1] ; break
                    old_bans = i["bans"] ; break
            database["config"].update_one({"bans": old_bans}, { "$pull": {"bans": str(userid)+"|"+str(reason)} })
            return '200'
        except:
            return '404'
    def is_banned(user_id):
        banned, reason = False, None
        for i in database["config"].find():
            if "bans" in list(i.keys()):
                for lists in i["bans"]:
                    if user_id == int(lists.split('|')[0]):
                        banned, reason = True, lists.split('|')[1] ;break
                break
        if banned:
            return reason
        else:
            return False
