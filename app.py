# app.py
import discord
import random
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = discord.Client(intents=intents)

# ── Constantes ────────────────────────────────────────────
MUDAE_ID = 432610292342587392

JEANNE_ALTER = ["jeanne d'arc (alter)", "jeanne alter", "jalter"]
JEANNE_ORIGINAL = ["jeanne d'arc"]

RESPONSES_ORIGINAL = [
    "...Esa impostora de luz apareció otra vez. Qué asco de recordatorio.",
    "La santa. Claro... como todo mundo la ama. Qué aburrido.",
    "Hmph. Ella otra vez. No me interesa.",
    "Qué conveniente. Justo el personaje que menos quería ver.",
    "La original. Qué predecible.",
]

RESPONSES_ALTER_SELF = [
    "Ah. Soy yo. Obviamente la mejor opción disponible.",
    "Claro que aparecí. El servidor tiene buen gusto. Esta vez.",
    "Yo. Naturalmente. No hace falta decir más.",
]

RESPONSES_LOVE_MASTER = {
    "gif": "img/jalter-talking.gif",
    "responses": [
        "¿Q-qué dices de repente, estúpido Master?! No es que me importe o algo así... pero... hmph.",
        "Eso no lo digas tan fácil. Las palabras tienen peso... idiota. Pero... no está mal escucharlo.",
        "¿Qué pretendes diciendo eso Master?! ...No te voy a responder. Pero tampoco te voy a quemar. Por hoy.",
        "Ugh. No hagas que me ruborice, Master. Es humillante.",
        "...Tch. Solo porque eres mi Master te perdono esa estupidez. No lo malinterpretes.",
    ]
}

RESPONSES_LOVE_STRANGER = {
    "gif": "img/jalter-jeanne-d-arc-alter.gif",
    "responses": [
        "¿Perdón? ¿Que acabas de decir? Qué asco.",
        "No eres mi Master. No me dirijas esas palabras. Nunca.",
        "Interesante forma de querer morir.",
        "Eso no te lo voy a responder. Pero si quieres que te queme, sigue hablando.",
        "Qué patético.",
        "Guarda eso para alguien que lo quiera escuchar. Yo no soy esa persona, Idiota suicida.",
    ]
}

RESPONSES = {
    "keywords": {
        "hola jalter": ["¿Me hablas a mí? Soy la única y verdadera Bruja del Dragón."],
        "hola juanita": ["¿A quién llamas Juanita? ¿Quieres convertirte en cenizas?"],
        "hola jeanne": ["¿Jeanne? ¿Quién es esa? No me suena de nada."],
        "jeanne": ["¿Jeanne? No me interesa esa impostora de luz. Solo yo soy la verdadera Bruja del Dragón."],
        "jalter": ["¿Me llamaste? Soy la única y verdadera Bruja del Dragón. No me compares con esa otra cosa."],
        "juana": ["¿Juana? ¿De verdad me hablas a mí? ¿Quieres que te queme?"],
        "jeanne d'arc": ["Agh, esa santa asquerosa otra vez..."],
        "que pasa jeanne": ["¿Qué pasa? ¿Quieres que te queme, estúpido? No soy tu amiga."],
    },
    "mention": [
        "¿Qué quieres ahora?",
        "Habla rápido.",
        "Qué molesto, ¿no tienes nada mejor que hacer?",
    ],
    "other_bot": [
        "Otro bot inútil. Qué sorpresa.",
        "¿Alguien pidió más basura automatizada?",
    ]
}

GIF_TRIGGERS = {
    "noble_phantasm": {
        "keywords": ["noble fantasma", "fantasma noble", "cual es tu noble", "noble phantasm"],
        "gif": "img/jalter-noble-phantasm.gif",
        "responses": [
            "¿Quieres ver mi Fantasma Noble? Hmph... está bien. Pero no digas que no te avisé. ¡La Grondement Du Haine!",
            "La Llama de la Bruja del Dragón. Observa bien, no lo repetiré. ¡La Grondement Du Haine!",
            "¿Eso quieres ver? De acuerdo. Que no se diga que no fui generosa. ¡La Grondement Du Haine!",
        ]
    },
    "ulti": {
        "keywords": ["ulti", "tira tu ulti", "cual es tu ulti", "tu ulti", "muestra tu ulti", "ultea"],
        "gif": "img/jeanne-alter-jeanne-darc-alter.gif",
        "responses": [
            "¿Mi ulti? ¿Lo llamas así? Qué vulgar. Pero bien... mira.",
            "Está bien. Solo porque me lo pediste correctamente.",
            "Hmph. No mereces verlo, pero haré una excepción.",
        ]
    },
    "insult": {
        "keywords": ["inútil", "eres mala", "te odio", "eres horrible", "cállate", "callate", "estúpida", "estupida", "idiota", "imbécil", "tonta", "patética", "fea"],
        "gif": "img/fgo-jalter.gif",
        "responses": [
            "¿Acabas de insultarme? Interesante decisión de vida.",
            "Repite eso y te convierto en cenizas. Tengo el poder para hacerlo.",
            "Qué valiente. O qué estúpido. Probablemente lo segundo.",
            "Nadie me habla así y sale ileso. Recuérdalo.",
        ]
    },
    "history": {
        "keywords": ["cuéntame tu historia", "dime tu historia", "quién eres", "quien eres", "cuéntame sobre ti"],
        "gif": "img/fate-grand-order.gif",
        "responses": [
            "¿Que quién soy? Soy la mujer que se levantó del fuego de la traición. "
            "La Bruja del Dragón que ahogará este mundo en llamas y cenizas. "
            "No me confundas con esa santa patética e hipócrita. "
            "Soy la Vengadora nacida del odio. Ahora dame una orden antes de que decida quemarte.",
        ]
    },
    "elogio": {
        "keywords": ["eres linda"],
        "gif": "img/jalter-grand-carnival.gif",
        "responses": [
            "¿Linda? No soy un adorno, soy la Bruja del Dragón. No me llames linda. Aunque naturalmente soy la más hermosa, por esta vez acepto tu elogio.",
            "Hmph. No creas que por adularme seré obediente pero... gra-gracias hjm estupid@",
        ]
    },
    "love": {
        "keywords": ["te amo", "te quiero", "me gustas", "eres mi favorita", "me encantas"],
        "gif": None,
        "responses": []  # vacío, lo manejamos aparte por lógica especial
    }
}

# ── Eventos ───────────────────────────────────────────────
@bot.event
async def on_guild_join(guild):
    channel = next(
        (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages),
        None
    )
    if channel:
        file = discord.File("img/jalter.png")
        embed = discord.Embed(
            description=(
                "¿Tú me invocaste? Hmph, supongo que serás mi Master.\n"
                "Soy Jeanne d'Arc, la Bruja del Dragón. No esperes que sea amable, estúpido.\n"
                "Si te pones en mi camino, te quemaré hasta las cenizas."
            ),
            color=0x8B0000
        )
        embed.set_image(url="attachment://jalter.png")
        await channel.send(file=file, embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # ── 1. Mudae ──────────────────────────────────────────
    if message.author.id == MUDAE_ID and message.embeds:
        embed = message.embeds[0]
        character_name = (embed.author.name or "").lower()

        if any(name in character_name for name in JEANNE_ALTER):
            master_id = os.getenv("MASTER_ID")
            await message.channel.send(
                f"<@{master_id}> {random.choice(RESPONSES_ALTER_SELF)}"
            )
            return

        if any(name in character_name for name in JEANNE_ORIGINAL):
            if "alter" not in character_name:
                await message.channel.send(random.choice(RESPONSES_ORIGINAL))
            return

    # ── 2. Otros bots ─────────────────────────────────────
    if message.author.bot:
        if random.random() < 0.01:
            await message.channel.send(random.choice(RESPONSES["other_bot"]))
        return

    content = message.content.lower()

    # ── 3. Menciones — todo lo demás requiere mención ─────
    if bot.user.mentioned_in(message):
        clean_content = content\
            .replace(f"<@{bot.user.id}>", "")\
            .replace(f"<@!{bot.user.id}>", "")\
            .strip()

        # Solo mención sin texto
        if not clean_content:
            await message.channel.send(random.choice(RESPONSES["mention"]))
            return

        # Triggers con gif
        for trigger_key, trigger_data in GIF_TRIGGERS.items():
            if any(kw in clean_content for kw in trigger_data["keywords"]):

                # Lógica especial para mensajes de amor
                if trigger_key == "love":
                    master_id = os.getenv("MASTER_ID")
                    is_master = str(message.author.id) == str(master_id)

                    pool = RESPONSES_LOVE_MASTER if is_master else RESPONSES_LOVE_STRANGER

                    response = random.choice(pool["responses"])
                    file = discord.File(pool["gif"])
                    await message.channel.send(content=response, file=file)
                    return

                # Resto de triggers normal
                response = random.choice(trigger_data["responses"])
                file = discord.File(trigger_data["gif"])
                await message.channel.send(content=response, file=file)
                return

        # Palabras clave
        for keyword, replies in RESPONSES["keywords"].items():
            if keyword in clean_content:
                await message.channel.send(random.choice(replies))
                return

        # Mencionaron pero no matcheó nada
        await message.channel.send(random.choice(RESPONSES["mention"]))
        return


bot.run(os.getenv("DISCORD_TOKEN"))