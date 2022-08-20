import os 
import discord
from discord.ext import commands
from discord_components import *
from discord_components import Button, ButtonStyle
import asyncio
from pymongo import MongoClient

server = input("[1] Servidor a usar (localhost) >> ")
MONGO_URI = f"mongodb://{server}"

client = MongoClient(MONGO_URI)
db_name = input("[2] Nombre de la Base de Datos (si no existe lo crea) >> ")
db = client[f"{db_name}"]

collection_user = db["users"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print("[+] DataBase bot online!!!")
    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄ 
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░   
    """)
    print("-------------------------------------------------------------------------------------------------------------")
    print("Bienvenido a Discord DB. Discord DB proporciona una base de datos para tu comunidad para porder almacenar cualquier tipo de información de su servidor. La colección que viene por defecto es una colección llamada 'users' que ahí almacena información de los usuarios cada vez que un miembro sea incorporado a su servidor.")
    print("Para acceder al menu de la Base de Datos, deberá ejecutar en el Discord el comando '-database' y se habrirá un canal donde aparecerá el menu de la Base de Datos.")
    print("-------------------------------------------------------------------------------------------------------------")
    DiscordComponents(bot)

@bot.event
async def on_member_join(member):
    collection_user.insert_one({"id":f"{member.id}","name":f"{member.name}","code":f"{member.discriminator}","fecha_de_incorporación":f"{member.joined_at}"})

@bot.command()
async def database(ctx):
    await ctx.message.delete()
    user = ctx.author
    if user.guild_permissions.administrator:
        main = True
        while main:
            guild = ctx.guild
            db_ch = await guild.create_text_channel(name=f"database_{user.name}")
            embed = discord.Embed(
                title="**BASE DE DATOS**",
                description="**Importante: **Para crear una colección en la Opción de Añadir Datos a una Colección cuando le pregunten por el nombre de la colección deberán introducir el nombre de la colección que quieren crear e insertar los primeros datos.",
                color=discord.Color.random()
            )
            embed.set_image(url="https://www.ikusi.com/wp-content/uploads/2022/05/base-datos-nube-1024x683.jpeg")
            embed.add_field(
                name="1. Ver Colección",
                value="Esta opción te permitirá ver los datos almacenados que hay en una colección.",
                inline=False
            )
            embed.add_field(
                name="2. Añadir Datos a una colección",
                value="Esta opción te permite añadir datos a una Colección.",
                inline=False
            )
            embed.add_field(
                name="3. Eliminar Datos",
                value="Esta opción te permitirá Eliminar Datos de una colección.",
                inline=False
            )
            embed.add_field(
                name="4. Actualizar Datos",
                value="Esta opción te permitirá actualizar datos de una colección.",
                inline=False
            )
            await bot.get_channel(db_ch.id).send(embed=embed, components = [[
                Button(label="Ver Coleccion", custom_id="opt1", style=ButtonStyle.green),
                Button(label="Añadir Datos a una Coleccion", custom_id="opt2", style=ButtonStyle.blue),
                Button(label="Eliminar Datos", custom_id="opt3", style=ButtonStyle.red),
                Button(label="Actualizar Dato", custom_id="opt4", style=ButtonStyle.gray),
                Button(label="Salir", custom_id="exit", style=ButtonStyle.grey)
            ]])
            try:
                interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id)
            except asyncio:
                return

            else:
                if interaction.custom_id == "opt1":
                    main = False
                    embed = discord.Embed(
                        title="**INTRODUCE EL NOMBRE DE LA COLECCIÓN**",
                        color=discord.Color.random()
                    )
                    await bot.get_channel(db_ch.id).send(embed=embed)
                    try:
                        message = await bot.wait_for("message", check=lambda message: message.author)
                    except asyncio:
                        return
                    else:
                        collection_name = message.content
                        collection = db[f"{collection_name}"]
                        result = collection.find()
                        for r in result:
                            embed = discord.Embed(
                                title="**RESULTADOS**",
                                description=f"{r}",
                                color=discord.Color.green()
                            )
                            await bot.get_channel(db_ch.id).send(embed=embed)
                        embed = discord.Embed(
                            title="**Seleccione una opción.**",
                            color=discord.Color.random()
                            )
                        await bot.get_channel(db_ch.id).send(embed=embed, components = [[
                            Button(label="Volver al menu de la Base de Datos", custom_id="return", style=ButtonStyle.green),
                            Button(label="Salir de la Base de Datos", custom_id="exit", style=ButtonStyle.red)
                        ]])
                        try:
                            interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id)
                        except asyncio:
                            return
                        else:
                            if interaction.custom_id == "return":
                                main = True
                                await db_ch.delete(reason=None)
                            elif interaction.custom_id == "exit":
                                await db_ch.delete(reason=None)

                elif interaction.custom_id == "opt2":
                    embed = discord.Embed(
                        title="**TERMINAL HABIERTO!!!**",
                        color=discord.Color.random()
                    )
                    await bot.get_channel(db_ch.id).send(embed=embed)
                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░
                    """)
                    collection_name = input(" [+] Nombre de la colección >> ")
                    if collection_name == "users":
                        embed = discord.Embed(
                            title="**Valla a la Terminal!!!**",
                            color=discord.Color.random()
                        )
                        await bot.get_channel(db_ch.id).send(embed=embed)
                        main = False
                        name = input("[+] Nombre del Usuario >> ")
                        code = input("[+] Codigo del usuario (debe tener 4 digitos) >> ")
                        fecha = input("[+] Fecha de incorporación a tu servidor >> ")
                        id_user = input("[+] Id del usuario >> ")
                        collection_user.insert_one({"id":f"{id_user}", "name":f"{name}", "code":f"{code}", "fecha_de_incorporacion":f"{fecha}"})
                        results = collection_user.find()
                        for r in results:
                            print(r)
                        a = input("[+] Presione intro para continuar >> ")
                        sele = True
                        while sele:
                            os.system("clear")
                            print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░
                            """)
                            print("""
------------------------------------------
[a] Volver al Menu de la Base de Datos

[b] Salir de la base de datos
------------------------------------------
                            """)
                            opt = input(" >> ")
                            if opt == "a":
                                sele = False
                                await db_ch.delete(reason=None)
                                main = True
                            
                            elif opt == "b":
                                sele = False
                                await db_ch.delete(reason=None)

                            else:
                                os.system("clear")

                    else:
                        collection = db[f"{collection_name}"]
                        activate1 = True
                        while activate1:
                            main = False
                            os.system("clear")
                            print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                            
                            """)
                            print("""
[+] SELECCIONE LA CANTIDAD DE DATOS QUE QUIERES AÑADIR
-----------------------------------------------------------
    [1]    [2]    [3]    [4]    [5]    [6]     [7]    [8] 
-----------------------------------------------------------
[+] 'exit' para volver al menu.
                            """)
                            num = input(" >>> ")
                            if num == "1":
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                a = input("[+] Presione intro para continuar >> ")
                                sele1 = True
                                while sele1:
                                    activate1 = False
                                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                                    
                                    """)
                                    print("""
----------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------
                                    """)
                                    opt = input(" >> ")
                                    if opt == "a":
                                        await db_ch.delete(reason=None)
                                        sele1 = False
                                        main = True
                                    elif opt == "b":
                                        sele1 = False
                                        await db_ch.delete(reason=None)
                                    else:
                                        os.system("clear")

                            elif num == "2": 
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                name2 = input("[2] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value2 = input("[2] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}",f"{name2}":f"{value2}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                    a = input("[+] Presione intro para continuar >> ")
                                    sele1 = True
                                    while sele1:
                                        activate1 = False
                                        print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░
                                        
                                        
                                        """)
                                        print("""
----------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------
                                    """)
                                    opt = input(" >> ")
                                    if opt == "a":
                                        await db_ch.delete(reason=None)
                                        sele1 = False
                                        main = True
                                    elif opt == "b":
                                        sele1 = False
                                        await db_ch.delete(reason=None)
                                    else:
                                        os.system("clear")

                            elif num == "3":
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                name2 = input("[2] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value2 = input("[2] Dato a insertar >> ")
                                name3 = input("[3] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value3 = input("[3] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}", f"{name2}":f"{value2}", f"{name3}":f"{value3}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                a = input("[+] Presione intro para continuar >> ")
                                sele1 = True
                                while sele1:
                                    activate1 = False
                                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                                    
                                    """)
                                    print("""
----------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------
                                    """)
                                    opt = input(" >> ")
                                    if opt == "a":
                                        await db_ch.delete(reason=None)
                                        sele1 = False
                                        main = True
                                    elif opt == "b":
                                        sele1 = False
                                        await db_ch.delete(reason=None)
                                    else:
                                        os.system("clear")
                             
                            elif num == "4":
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                name2 = input("[2] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value2 = input("[2] Dato a insertar >> ")
                                name3 = input("[3] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value3 = input("[3] Dato a insertar >> ")
                                name4 = input("[4] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value4 = input("[4] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}", f"{name2}":f"{value2}", f"{name3}":f"{value3}", f"{name4}":f"{value4}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                a = input("[+] Presione intro para continuar >> ")
                                sele1 = True
                                while sele1:
                                    activate1 = False
                                    os.system("clear")
                                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                                    
                                    """)
                                    print("""
----------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------
                                    """)
                                    opt = input(" >> ")
                                    if opt == "a":
                                        await db_ch.delete(reason=None)
                                        sele1 = False
                                        main = True
                                    elif opt == "b":
                                        sele1 = False
                                        await db_ch.delete(reason=None)
                                    else:
                                        os.system("clear")

                            elif num == "5":
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                name2 = input("[2] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value2 = input("[2] Dato a insertar >> ")
                                name3 = input("[3] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value3 = input("[3] Dato a insertar >> ")
                                name4 = input("[4] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value4 = input("[4] Dato a insertar >> ")
                                name5 = input("[5] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value5 = input("[5] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}", f"{name2}":f"{value2}", f"{name3}":f"{value3}", f"{name4}":f"{value4}",f"{name5}":f"{value5}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                    a = input("[+] Presione intro para continuar >> ")
                                    sele1 = True
                                    while sele1:
                                        activate1 = False
                                        print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                                        
                                        """)
                                        print("""
----------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------
                                        """)
                                        opt = input(" >> ")
                                        if opt == "a":
                                            await db_ch.delete(reason=None)
                                            sele1 = False
                                            main = True
                                        elif opt == "b":
                                            sele1 = False
                                            await db_ch.delete(reason=None)
                                        else:
                                            os.system("clear")


                            elif num == "6":
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                name2 = input("[2] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value2 = input("[2] Dato a insertar >> ")
                                name3 = input("[3] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value3 = input("[3] Dato a insertar >> ")
                                name4 = input("[4] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value4 = input("[4] Dato a insertar >> ")
                                name5 = input("[5] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value5 = input("[5] Dato a insertar >> ")
                                name6 = input("[6] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value6 = input("[6] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}", f"{name2}":f"{value2}", f"{name3}":f"{value3}",f"{name4}":f"{value4}", f"{name5}":f"{value5}", f"{name6}":f"{value6}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                a = input("[+] Presione intro para continuar >> ")
                                sele1 = True
                                while sele1:
                                    activate1 = False
                                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░
                                    """)
                                    print("""
----------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------
                                    """)
                                    opt = input(" >> ")
                                    if opt == "a":
                                        await db_ch.delete(reason=None)
                                        sele1 = False
                                        main = True
                                    elif opt == "b":
                                        sele1 = False
                                        await db_ch.delete(reason=None)
                                    else:
                                        os.system("clear")

                            elif num == "7":
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                name2 = input("[2] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value2 = input("[2] Dato a insertar >> ")
                                name3 = input("[3] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value3 = input("[3] Dato a insertar >> ")
                                name4 = input("[4] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value4 = input("[4] Dato a insertar >> ")
                                name5 = input("[5] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value5 = input("[5] Dato a insertar >> ")
                                name6 = input("[6] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value6 = input("[6] Dato a insertar >> ")
                                name7 = input("[7] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value7 = input("[7] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}", f"{name2}":f"{value2}", f"{name3}":f"{value3}", f"{name4}":f"{value4}", f"{name5}":f"{value5}", f"{name6}":f"{value6}", f"{name7}":f"{value7}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                a = input("[+] Presione intro para continuar >> ")
                                sele1 = True
                                while sele1:
                                    activate1 = False
                                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                                    
                                    """)
                                    print("""
----------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------
                                    """)
                                    opt = input(" >> ")
                                    if opt == "a":
                                        await db_ch.delete(reason=None)
                                        sele1 = False
                                        main = True
                                    elif opt == "b":
                                        sele1 = False
                                        await db_ch.delete(reason=None)
                                    else:
                                        os.system("clear")

                            elif num == "8":
                                name1 = input("[1] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value1 = input("[1] Dato a insertar >> ")
                                name2 = input("[2] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value2 = input("[2] Dato a insertar >> ")
                                name3 = input("[3] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value3 = input("[3] Dato a insertar >> ")
                                name4 = input("[4] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value4 = input("[4] Dato a insertar >> ")
                                name5 = input("[5] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value5 = input("[5] Dato a insertar >> ")
                                name6 = input("[6] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value6 = input("[6] Dato a insertar >> ")
                                name7 = input("[7] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value7 = input("[7] Dato a insertar >> ")
                                name8 = input("[8] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                                value8 = input("[8] Dato a insertar >> ")
                                collection.insert_one({f"{name1}":f"{value1}", f"{name2}":f"{value2}", f"{name3}":f"{value3}", f"{name4}":f"{value4}", f"{name5}":f"{value5}", f"{name6}":f"{value6}", f"{name7}":f"{value7}", f"{name8}":f"{value8}"})
                                result = collection.find()
                                for r in result:
                                    print(r)
                                    a = input("[+] Presiona intro para continuar >> ")
                                    sele1 = True
                                    while sele1:
                                        activate1 = False
                                        print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                                        
                                        """)
                                        print("""
----------------------------------------
[a] Volver al menu de la Base de Datos.

[b] Salir de la Base de Datos.
----------------------------------------
                                    """)
                                    opt = input(" >> ")
                                    if opt == "a":
                                        await db_ch.delete(reason=None)
                                        sele1 = False
                                        main = True
                                    elif opt == "b":
                                        sele1 = False
                                        await db_ch.delete(reason=None)
                                    else:
                                        os.system("clear")


                            elif num == "exit":
                                activate1 = False
                                main = False
                                os.system("clear")
                                await db_ch.delete(reason=None)
                        
                            else:
                                os.system("clear")
            
                elif interaction.custom_id == "opt3":
                    embed = discord.Embed(
                        title="**Valla a la Terminal.**",
                        color=discord.Color.random()
                    )
                    await bot.get_channel(db_ch.id).send(embed=embed)
                    os.system("clear")
                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                    
                    """)
                    collection_name = input("[+] Nombre de la colección >> ")
                    collection = db[f'{collection_name}']
                    result = collection.find()
                    for r in result:
                        print(f"""
-----------------------------------------------------------
{r}
-----------------------------------------------------------
                        """)
                        name = input("[+] Nombre del tipo de dato >> ")
                        value = input("[+] Valor del dato >> ")
                        collection.delete_one({f"{name}":f"{value}"})
                        result = collection.find()
                        for r in result:
                            print(r)
                        a = input("[+] Presione intro para continuar >>")
                        activate2 = True
                        while activate2:
                            os.system("clear")
                            main = False
                            print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                            
                            """)
                            print("""
-----------------------------------------
[a] Volver al menu de la Base de Datos 
                        
[b] Salir de la base de datos
------------------------------------------
                            """)
                        opt = input(" >> ")
                        if opt == "a":
                            await db_ch.delete(reason=None)
                            activate2 = False
                            main = True
                        elif opt == "b":
                            await db_ch.delete(reason=None)
                            activate2 = False
                        else:
                            os.system("clear")
                
                elif interaction.custom_id == "opt4":
                    embed = discord.Embed(
                        title="**Valla a la Terminal**",
                        color=discord.Color.random()
                    )
                    await bot.get_channel(db_ch.id).send(embed=embed)
                    os.system("clear")
                    print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░                    
                    """)
                    collection_name = input("[+] Nombre de la colección >> ")
                    collection = db[f"{collection_name}"]
                    result = collection.find()
                    for r in result:
                        print(r)
                    name = input("[+] Tipo de dato (nombre, apellido, edad, etc.) >> ")
                    value = input("[+] Valor del dato >> ")
                    name_up = input("[1] Tipo de dato a actualizar >> ")
                    value_up = input("[1] Nuevo dato a actualizar >> ")
                    collection.update_one({f"{name}":f"{value}"}, {"$set": {f"{name_up}":f"{value_up}"}})
                    result = collection.find()
                    for r in result:
                        print("----------------------------------------------------------------------------")
                        print(r)
                        print("----------------------------------------------------------------------------")
                        a = input("[+] Presione intro para continuar >> ")
                        activate3 = True
                        while activate3:
                            os.system("clear")
                            main = False
                            print("""
█▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄   █▀▀▄ █▀▀▄
█░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█   █░░█ █▀▀▄
▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░   ▀▀▀░ ▀▀▀░
                            
                            """)
                            print("""
----------------------------------------------
[a] Volver al menu de la Base de Datos

[b] Salir de la Base de datos
----------------------------------------------   
                            """)
                            opt = input(" >>> ")
                            if opt == "a":
                                main = True
                                activate3 = False
                                await db_ch.delete(reason=None)
                            
                            elif opt == "b":
                                activate3 = False
                                await db_ch.delete(reason=None)
                            
                            else:
                                os.system("clear")

                elif interaction.custom_id == "exit":
                    await db_ch.delete(reason=None)
                    main = False

    else:
        error = discord.Embed(
            title="**NO TIENES PERMISO PARA ACCEDER A LA BASE DE DATOS!!!!**",
            color=discord.Color.red()
        )
        await ctx.send(embed=error, delete_after=10)
        

bot.run("inserte-el-token-de-su-bot")