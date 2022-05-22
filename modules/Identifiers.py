class Identifiers:
    class tribulle:
        class send:
            ET_ResultatIdentificationService = 2
            ET_ResultatMiseAJourLocalisation = 5
            ET_ResultatMiseAJourLocalisations = 7
            ET_ResultatMessageCanal = 21
            ET_SignaleMessageCanal = 22
            ET_ResultatRejoindreCanal = 24
            ET_ResultatQuitterCanal = 26
            ET_SignaleRejointCanal = 27
            ET_SignaleQuitteCanal = 28
            ET_SignaleMembreRejointCanal = 29
            ET_SignaleMembresRejoignentCanal = 30
            ET_SignaleMembreQuitteCanal = 31
            ET_SignaleMembresQuittentCanal = 32
            ET_ResultatMessagePrive = 34
            ET_RecoitMessagePriveSysteme = 35
            ET_RecoitMessagePrive = 36
            ET_ResultatDefinitModeSilence = 40
            ET_ResultatDemandeMembresCanal = 42
            ET_ErreurDemandeMembresCanal = 43
            ET_ResultatAjoutAmi = 45
            ET_ResultatRetireAmi = 47
            ET_ResultatListeAmis = 49
            ET_ErreurListeAmis = 50
            ET_SignaleAjoutAmi = 51
            ET_SignaleModificationLocalisationAmi = 52
            ET_SignaleRetraitAmi = 53
            ET_SignaleConnexionAmi = 54
            ET_SignaleDeconnexionAmi = 55
            ET_SignaleConnexionAmis = 56
            ET_SignaleDeconnexionAmis = 57
            ET_SignaleAjoutAmiBidirectionnel = 58
            ET_SignaleRetraitAmiBidirectionnel = 59
            ET_ResultatDemandeEnMariage = 61
            ET_ErreurDemandeEnMariage = 62
            ET_SignaleDemandeEnMariage = 63
            ET_ResultatRepondDemandeEnMariage = 65
            ET_SignaleMariage = 66
            ET_ResultatDemandeDivorce = 68
            ET_SignaleDivorce = 69
            ET_ResultatAjoutListeNoire = 71
            ET_ResultatRetireListeNoire = 73
            ET_ResultatListeNoire = 75
            ET_ErreurListeNoire = 76
            ET_SignaleAjoutListeNoire = 77
            ET_SignaleRetraitListeNoire = 78
            ET_CreerTribu = 79
            ET_ResultatCreerTribu = 80
            ET_SignaleTribuCreee = 81
            ET_SignaleInvitationTribu = 82
            ET_ErreurRepondInvitationTribu = 84
            ET_ResultatInformationsTribu = 86
            ET_ErreurInformationsTribu = 87
            ET_ResultatInformationsTribuSimple = 89
            ET_ErreurInformationsTribuSimple = 90
            ET_ResultatMembresTribu = 92
            ET_ErreurMembresTribu = 93
            ET_ResultatQuitterTribu = 95
            ET_ResultatListeHistoriqueTribu = 97
            ET_ErreurListeHistoriqueTribu = 98
            ET_SignaleConnexionMembre = 99
            ET_SignaleDeconnexionMembre = 100
            ET_SignaleConnexionMembres = 101
            ET_SignaleDeconnexionMembres = 102
            ET_SignaleChangementMessageJour = 103
            ET_SignaleChangementCodeMaisonTFM = 104
            ET_SignaleChangementRang = 105
            ET_SignaleExclusion = 106
            ET_SignaleNouveauMembre = 107
            ET_SignaleDepartMembre = 108
            ET_SignaleModificationLocalisationMembreTribu = 109
            ET_ResultatChangerMessageJour = 111
            ET_ResultatExclureMembre = 115
            ET_ResultatInviterMembre = 117
            ET_ErreurInviterMembre = 118
            ET_ResultatChangerCodeMaisonTFM = 120
            ET_ResultatListeRangs = 122
            ET_ErreurListeRangs = 123
            ET_ResultatAffecterRang = 125
            ET_ResultatAjouterRang = 127
            ET_ErreurAjouterRang = 128
            ET_ResultatSupprimerRang = 130
            ET_ResultatRenommerRang = 132
            ET_ResultatAjouterDroitRang = 134
            ET_ResultatSupprimerDroitRang = 136
            ET_ResultatInverserOrdreRangs = 138
            ET_ResultatDesignerChefSpirituel = 142
            ET_ResultatRenommerTribu = 144
            ET_ResultatDissoudreTribu = 146
            ET_SignaleDissolutionTribu = 147
            ET_ResultatDonneesUtilisateur = 153
            ET_ErreurDonneesUtilisateur = 154
            ET_ResultatDefinitDonneesUtilisateur = 156
            ET_ResultatChangerDeGenre = 158
            ET_SignaleChangementAvatar = 160
            ET_SignaleChangementDeGenre = 159
            ET_DemandeNouveauxMessagesPrivesWeb = 161
            ET_DemandeNouveauxMessagesPrivesWebEnMasse = 162
            ET_SignalNouveauxMessagesPrivesWeb = 163
            ET_SignalNouveauMessagePriveWeb = 164
            ET_ReponseDemandeInfosJeuUtilisateur = 166
            ET_ErreurDemandeInfosJeuUtilisateur = 167
        
        class recv:
            ST_IdentificationService = 1
            ST_PingUtilisateur = 3
            ST_MiseAJourLocalisation = 4
            ST_MiseAJourLocalisations = 6
            ST_EnvoitMessageCanal = 20
            ST_RejoindreCanal = 23
            ST_QuitterCanal = 25
            ST_EnvoitMessagePrive = 33
            ST_DefinitModeSilence = 39
            ST_DemandeMembresCanal = 41
            ST_AjoutAmi = 44
            ST_RetireAmi = 46
            ST_ListeAmis = 48
            ST_DemandeEnMariage = 60
            ST_RepondDemandeEnMariage = 64
            ST_DemandeDivorce = 67
            ST_AjoutListeNoire = 70
            ST_RetireListeNoire = 72
            ST_ListeNoire = 74
            ST_CreerTribu = 79
            ST_ResultatCreerTribu = 80
            ST_RepondInvitationTribu = 83
            ST_DemandeInformationsTribu = 85
            ST_DemandeInformationsTribuSimpleParNom = 88
            ST_DemandeMembresTribu = 91
            ST_QuitterTribu = 94
            ST_ListeHistoriqueTribu = 96
            ST_ChangerMessageJour = 110
            ST_ExclureMembre = 114
            ST_InviterMembre = 116
            ST_ChangerCodeMaisonTFM = 119
            ST_ListeRangs = 121
            ST_AffecterRang = 124
            ST_AjouterRang = 126
            ST_SupprimerRang = 129
            ST_RenommerRang = 131
            ST_AjouterDroitRang = 133
            ST_SupprimerDroitRang = 135
            ST_InverserOrdreRangs = 137
            ST_DesignerChefSpirituel = 141
            ST_RenommerTribu = 143
            ST_DissoudreTribu = 145
            ST_DemandeDonneesUtilisateur = 152
            ST_DefinitDonneesUtilisateur = 155
            ST_ChangerDeGenre = 157
            ST_SignaleChangementDeGenre = 159
            ST_SignaleChangementAvatar = 160
            ST_SignalNouveauxMessagesPrivesWeb = 163
            ST_SignalNouveauMessagePriveWeb = 164
            ST_RequeteDemandeInfosJeuUtilisateur = 165
            
    class recv:
        class Old_Protocol:
            C = 1
            Old_Protocol = 1
        
        class Sync:
            C = 4
            Object_Sync = 3
            Mouse_Movement = 4
            Mort = 5
            Shaman_Position = 8
            Crouch = 9
        
        class Room:
            C = 5
            Shaman_Message = 9
            Convert_Skill = 14
            Demolition_Skill = 15
            Projection_Skill = 16
            Enter_Hole = 18
            Get_Cheese = 19
            Place_Object = 20
            Ice_Cube = 21
            Defilante_Points = 25
            Restorative_Skill = 26
            Recycling_Skill = 27
            Gravitational_Skill = 28
            Antigravity_Skill = 29
            Handymouse_Skill = 35
            Enter_Room = 38
            Room_Passowrd = 39
            Send_Music = 70
            Music_Time = 71
            Send_PlayList = 73
        
        class Chat:
            C = 6
            Chat_Message = 6
            Staff_Chat = 10
            Commands_Chat = 26
 
        class Player:
            C = 8
            Emote = 1
            Langue = 2
            Emotions = 5
            Shaman_Fly = 15
            Shop_List = 20
            Buy_Skill = 21
            Redistribute = 22
            Report = 25
            Ping = 30
            Meep = 39
            Vampire = 66
        
        class Buy_Fraises:
            C = 12
            Buy_Fraises = 10
        
        class Tribe_House:
            C = 16
            Tribe_House = 1
            
        class Shop:
            C = 20
            Equip_Clothe = 6
            Save_Clothe = 7
            Info = 15
            Equip_Item = 18
            Buy_Item = 19
            Buy_Custom = 20
            Custom_Item = 21
            Buy_Clothe = 22
            Buy_Shaman_Item = 23
            Equip_Shaman_Item = 24
            Buy_Shaman_Custom = 25
            Custom_Shaman_Item = 26
            Send_Gift = 28
            Gift_Result = 29
        
        class Modopwet:
            C = 25
            Modopwet = 2
            Delete_Report = 23
            Watch = 24
            Ban_Hack = 25
            Change_Langue = 26
            Chat_Log = 27
        
        class Login:
            C = 26
            Create_Account = 7
            Login = 8
            Player_FPS = 13
            Captcha = 20
            Player_Info = 28
            Player_Info2 = 29
            Game_Mode = 35
            Request_Info = 40
        
        class Transformation:
            C = 27
            Transformation_Object = 11
        
        class Informations:
            C = 28
            Game_Log = 4
            Change_Shaman_Type = 10
            Send_Email = 11
            Validate_Code = 12
            Change_Pass = 14
            Navidad_Letter = 15
            Send_Code = 16
            Computer_Info = 17
            Change_Shaman_Color = 18
            Recovery_Password = 40
            Recovery_Password_Code = 41
            Recovery_Password_Change = 42
            Informations = 50
        
        class Lua:
            C = 29
            Lua_Script = 1
            Key_Board = 2
            Mouse_Click = 3
            Popup_Answer = 20
            Text_Area_Callback = 21
            Color_Picked = 32
        
        class Cafe:
            C = 30
            Mulodrome_Close = 13
            Mulodrome_Join = 15
            Mulodrome_Leave = 17
            Mulodrome_Play = 20
            Reload_Cafe = 40
            Open_Cafe_Topic = 41
            Create_New_Cafe_Post = 43
            Create_New_Cafe_Topic = 44
            Open_Cafe = 45
            Vote_Cafe_Post = 46
        
        class Inventory:
            C = 31
            Open_Inventory = 1
            Use_Consumable = 3
            Equip_Consumable = 4
            Trade_Invite = 5
            Cancel_Trade = 6
            Trade_Add_Consusmable = 8
            Trade_Result = 9
        
        class Tribulle:
            C = 60
            Tribulle = 1
            
        class Transformice:
            C = 100
            Invocation = 2
            Remove_Invocation = 3
            Shaman_Symbol = 79
            Mort_Mouse = 80
            Village_NPC = 75

    class send:
        send_Banner = [16, 9]
        Sync = [4, 3]
        Player_Movement = [4, 4]
        Move_Object = [4, 7]
        Remove_Object = [4, 8]
        Crouch = [4, 9]
        Shaman_Position = [4, 10]
        Rounds_Count = [5, 1]
        New_Map = [5, 2]
        Shaman_Message = [5, 9]
        Map_Start_Timer = [5, 10]
        Convert_Skill = [5, 13]
        Skill_Object = [5, 14]
        Demolition_Skill = [5, 15]
        Projection_Skill = [5, 16]
        Explosion = [5, 17]
        Spawn_Object = [5, 20]
        Enter_Room = [5, 21]
        Round_Time = [5, 22]
        Snow = [5, 23]
        Restorative_Skill = [5, 26]
        Recycling_Skill = [5, 27]
        Gravitation_Skill = [5, 28]
        Antigravity_Skill = [5, 29]
        Rollout_Mouse_Skill = [5, 30]
        Mouse_Size = [5, 31]
        Remove_All_Objects_Skill = [5, 32]
        Leaf_Mouse_Skill = [5, 33]
        Iced_Mouse_Skill = [5, 34]
        Handymouse_Skill = [5, 35]
        Spider_Mouse_Skill = [5, 36]
        Grapnel_Mouse_Skill = [5, 37]
        Room_Password = [5, 39]
        Skill = [5, 40]
        Reset_Shaman_Skills = [5, 42]
        Gatman_Skill = [5, 43]
        Storm = [5, 44]
        Bonfire_Skill = [5, 45]
        Teleport = [5, 50]
        Candies = [5, 51]
        Lower_Sync_Delay = [5, 52]
        Video_In_Room = [5, 72]
        Music_PlayList = [5, 73]
        All_Chat = [6, 6]
        Message = [6, 9]
        Staff_Chat = [6, 10]
        Time_20Sec = [6, 17]
        Room_Game_Mode = [7, 1]
        Room_Type = [7, 30]
        Player_Emote = [8, 1]
        Give_Currency = [8, 2]
        Move_Player = [8, 3]
        Emotion = [8, 5]
        Player_Got_Cheese = [8, 6]
        Set_Player_Score = [8, 7]
        Shaman_Exp = [8, 8]
        Shaman_Gain_Exp = [8, 9]
        Enable_Skill = [8, 10]
        Shaman_Info = [8, 11]
        Titles_List = [8, 14]
        Change_Title = [100, 72]
        Shaman_Fly = [8, 15]
        Profile = [8, 16]
        Remove_Cheese = [8, 19]
        Shop_List = [8, 20]
        Shaman_Skills = [8, 22]
        NPC = [8, 30]
        Meep = [8, 38]
        Can_Meep = [8, 39]
        Unlocked_Badge = [8, 42]
        Don = [8, 43]
        Anim_Zelda = [8, 44]
        Vampire_Mode = [8, 66]
        Item_Buy = [20, 2]
        Promotion = [20, 3]
        Shop_Info = [20, 15]
        Look_Change = [20, 17]
        Shaman_Look = [20, 24]
        Shaman_Items = [20, 27]
        Gift_Result = [20, 29]
        Shop_Gift = [20, 30]
        Shop_GIft_Message = [20, 31]
        Shaman_Earned_Exp = [24, 1]
        Shaman_Earned_Level = [24, 2]
        Redistribute_Error_Time = [24, 3]
        Redistribute_Error_Cheeses = [24, 4]
        Open_Modopwet = [25, 2]
        Modopwet_Banned = [25, 5]
        Modopwet_Disconnected = [25, 6]
        Modopwet_Deleted = [25, 7]
        Modopwet_Chatlog = [25, 10]
        Player_Identification = [26, 2]
        Correct_Version = [26, 3]
        First_Count = [26, 10]
        Spawn_Monster = [26, 6]
        Remove_Monster = [26, 7]
        Move_Monster = [26, 8]
        Can_Gift = [26, 10]
        Login_Result = [26, 12]
        Captcha = [26, 20]
        Tribulle_Token = [26, 41]
        Images = [26, 31]
        Login_Souris = [26, 33]
        Login_Info = [26, 33]
        Game_Mode = [26, 35]
        Open_NPC_Shop = [26, 38]
        Can_Transformation = [27, 10]
        Transformation = [27, 11]
        Time_Stamp = [28, 2]
        Promotion_Popup = [28, 3]
        Message_Langue = [28, 5]
        Mod_Mute = [28, 8]
        Shaman_Type = [28, 10]
        Code_Validated = [28, 12]
        Email_Confirmed = [28, 13]
        Navidad_Letter = [28, 15]
        Send_Email = [28, 16]
        Email_Sended = [28, 17]
        Message_Langue_Error = [28, 28]
        Recovery_Password = [28, 40]
        Log_Message = [28, 46]
        Request_Info = [28, 50]
        Server_Restart = [28, 88]
        Bind_Key_Board = [29, 2]
        Bind_Mouse = [29, 3]
        Set_Name_Color = [29, 4]
        Lua_Message = [29, 6]
        Remove_Image = [29, 18]
        Add_Image = [29, 19]
        Add_Text_Area = [29, 20]
        Update_Text_Area = [29, 21]
        Remove_Text_Area = [29, 22]
        Add_Popup = [29, 23]
        Set_UI_Map_Name = [29, 25]
        Set_UI_Shaman_Name = [29, 26]
        Display_Particle = [29, 27]
        Add_Physic_Object = [29, 28]
        Remove_Physic_Object = [29, 29]
        Add_Joint = [29, 30]
        Remove_Joint = [29, 31]
        Show_Color_Picker = [29, 32]
        Mulodrome_Result = [30, 4]
        Mulodrome_End = [30, 13]
        Mulodrome_Start = [30, 14]
        Mulodrome_Join = [30, 15]
        Mulodrome_Leave = [30, 16]
        Mulodrome_Winner = [30, 21]
        Cafe_Topics_List = [30, 40]
        Open_Cafe_Topic = [30, 41]
        Open_Cafe = [30, 42]
        Cafe_New_Post = [30, 44]
        Inventory = [31, 1]
        Update_Inventory_Consumable = [31, 2]
        Use_Inventory_Consumable = [31, 3]
        Trade_Invite = [31, 5]
        Trade_Result = [31, 6]
        Trade_Start = [31, 7]
        Trade_Add_Consumable = [31, 8]
        Trade_Confirm = [31, 9]
        Trade_Close = [31, 10]
        Mouse_Color = [29, 32]
        Bulle = [44, 1]
        Bulle_ID = [44, 22]
        Tribulle = [60, 1]
        Rainbow = [79, 31]
        Invocation = [100, 2]
        Remove_Invocation = [100, 3]
        Joquempo = [100, 5]
        Crazzy_Packet = [100, 40]
        New_Consumable = [100, 67]
        Consumable_Angel = [100, 70]
        Consumable_Balao = [100, 71]
        Consumable_Henna = [100, 69]
        Consumable_Clock = [100, 40]
        Election = [100, 80]
        Select_Election = [100, 81]
        Shop_Steam = [100, 90]
    
    class old:
        class recv:
            class AFK:
                C = 4
                Bomb_Explode = 6
                AFK_Player = 10
                Conjure_Start = 12
                Conjure_End = 13
                Conjuration = 14
                Snow_Ball = 16
            
            class Anchors:
                C = 5
                Anchors = 7
                Begin_Spawn = 8
                Spawn_Cancel = 9
                Old_Packet = 15
                Death = 14
                Totem_Anchors = 13
                Move_Cheese = 16
                Bombs = 17
            
            class Commands:
                C = 6
                Commands = 26
            
            class Balloons:
                C = 8
                Place_Balloon = 16
                Balloon_Placed = 17
            
            class Map:
                C = 14
                Vote_Map = 4
                Load_Map = 6
                Validate_Map = 10
                Send_XML = 11
                Return_To_Editeur = 14
                Export_Map = 18
                Reset_Map = 19
                Exit_Editeur = 26
            
            class Draw:
                C = 25
                Clear = 3
                Drawing = 4
                Point = 5
            
            class Dummy:
                C = 26
                Dummy = 2

        class send:
            Bomb_Explode = [4, 6]
            Conjure_Start = [4, 12]
            Conjure_End = [4, 13]
            Add_Conjuration = [4, 14]
            Conjuration_Destroy = [4, 15]
            Anchors = [5, 7]
            Begin_Spawn = [5, 8]
            Spawn_Cancel = [5, 9]
            Death = [5, 14]
            Old_Packet = [5, 15]
            Sync_Old = [5, 22]
            Move_Cheese = [5, 16]
            Bombs = [5, 17]
            Player_Get_Cheese = [5, 19]
            Tutorial = [5, 90]
            Message = [6, 20]
            Balloon_Placed = [8, 2]
            Player_Died = [8, 5]
            Player_Disconnect = [8, 7]
            Player_Respawn = [8, 8]
            Player_List = [8, 9]
            Change_Title = [8, 13]
            Unlocked_Title = [8, 14]
            Titles_List = [8, 15]
            Place_Balloon = [8, 16]
            Shaman_Perfomance = [8, 17]
            Save_Remaining = [8, 18]
            Sync = [8, 21]
            Catch_The_Cheese_Map = [8, 23]
            Vote_Box = [14, 4]
            Map_Exported = [14, 5]
            Load_Map_Result = [14, 8]
            Load_Map = [14, 9]
            Editeur = [14, 14]
            Map_Editor = [14, 14]
            Map_Validated = [14, 17]
            Editeur_Message = [14, 20]
            Change_Tribe_Code_Result = [16, 4]
            Totem = [22, 22]
            Drawing_Clear = [26, 3]
            Drawing = [26, 4]
            Drawing_Point = [26, 5]
            Player_Ban_Message = [26, 7]
            Login = [26, 8]
            Ban_Consideration = [26, 9]
            Halloween_Player_Damanged = [26, 11]
            Music = [26, 12]
            Player_Ban = [26, 17]
            Player_Ban_Login = [26, 18]
            Log = [26, 23]
            Totem_Item_Count = [28, 11]
