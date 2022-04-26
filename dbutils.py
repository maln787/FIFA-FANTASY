import os
from dotenv import load_dotenv

load_dotenv()
DB_CONN = {
        'host':'localhost',
        'user':'root', 
        'password' : "root@123",
        'db':'FIFA'
}


class Query:
    USER_REGISTER = """INSERT INTO `user` 
                        VALUES (NULL, %s, %s, %s, %s, %s)""".strip()

    USER_LOGIN = """SELECT * 
                    FROM `user` 
                    WHERE username = %s 
                    AND password = %s""".strip()

    USER_CHECK_ACC = """SELECT * 
                        FROM `user` 
                        WHERE username = %s""".strip()

    PLAYER_SEARCH = """ SELECT * 
                        FROM `main_df`
                        WHERE player_name = %s
                        AND RIGHT(player_id,2) = %s""".strip()

    POSITION = """ SELECT positions
                   FROM `positions`
                   WHERE player_id = %s""".strip()
    CLUB = """ SELECT *
               FROM `club`
               WHERE player_id = %s""".strip()

    INSERTPLAYER = """ INSERT INTO `user_team`
                       (user_id, player_id)
                       VALUES (%s, %s)""".strip()

    FETCHTEAM = """ SELECT player_id FROM `user_team` WHERE user_id = %s""".strip()

    TEAMSHOW = """ WITH cte as (SELECT * from `main_df` 
                   WHERE player_id = %s)

                   SELECT player_id, 
                          player_name, 
                          club_name, 
                          league_name, 
                          nationality_name, 
                          overall 
                   FROM cte 
                        JOIN club USING(player_id)""".strip()
    
    SQUADNAME = """INSERT INTO `squad`
                   (user_id, squad_name)
                   VALUES (%s,%s)""".strip()

    FETCHSQNAME = """SELECT * 
                     FROM `squad`
                     WHERE user_id = %s""".strip()
                     
    UPDATESQUAD = """UPDATE `squad`
                     SET squad_name = %s
                     WHERE user_id = %s""".strip()


