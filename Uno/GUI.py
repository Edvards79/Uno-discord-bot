import random
import PIL
from PIL import Image, ImageFont, ImageDraw
from matplotlib import font_manager

from Uno.Game import Game
from Uno.Player import Player
from Uno.Deck import Card, Deck


class GUI:

    @staticmethod
    def generate_table_image(game):
        table_img = Image.open('Uno/assets/Table_4.png', 'r')
        card_imgs = GUI._load_card_images(game.table)
        composite = Image.new('RGBA', table_img.size, (0, 0, 0, 0))
        composite.paste(table_img, (0,0))

        for card_img in card_imgs:
            # Resize the card
            new_card_size = tuple(ti//4 for ti in card_img.size)
            card_img = card_img.resize(new_card_size)

            # Rotate the card randomly
            card_img = card_img.rotate(random.randint(-20, 20), PIL.Image.NEAREST, expand = 1)

            # Calculate the middle position
            position_x = table_img.size[0] // 2 - new_card_size[0] // 2
            position_y = table_img.size[1] // 2 - new_card_size[1] // 2

            # Randomly adjust card's position
            position_x += random.randint(-30, 30)
            position_y += random.randint(-30, 30)

            composite.paste(card_img, (position_x, position_y), mask=card_img)

        # Add deck to the composite image
        deck_img = Image.open('Uno/assets/Deck.png', 'r')
        new_deck_size = tuple(ti//4 for ti in deck_img.size)
        deck_img = deck_img.resize(new_deck_size)
        deck_position = (table_img.size[0] // 2 - 200, table_img.size[1] // 2 - 50)
        composite.paste(deck_img, deck_position, mask=deck_img)

        return composite
    
    @staticmethod
    def generate_player_view_image(player, table_img, text=None):
        card_imgs = GUI._load_card_images(player.hand)
        composite = Image.new('RGBA', table_img.size, (0, 0, 0, 0))
        composite.paste(table_img, (0,0))
        current_x = table_img.size[0] // 2 - 200
        for card_img in card_imgs:
            # Resize the card
            new_card_size = tuple(ti//4 for ti in card_img.size)
            card_img = card_img.resize(new_card_size)

            # Calculate position
            position = (current_x, 520)
            current_x += 50

            composite.paste(card_img, position, mask=card_img)
        
        if text:
            # Add text to the composite image
            draw = ImageDraw.Draw(composite)
            font = font_manager.FontProperties(family='sans-serif', weight='bold')
            file = font_manager.findfont(font)

            font = ImageFont.truetype(file, 30)
            w, h = draw.textsize(text, font=font)
            position = ((table_img.size[0]-w)/2, 150)
            draw.text(position, text, (255,255,255), font=font)

        return composite

    staticmethod
    def _load_card_images(cards):
        card_images = []
        for card in cards:
            if card.value == Card.CARD_WILD:
                card_images.append(Image.open('Uno/assets/Wild.png', 'r'))
            elif card.value == Card.CARD_DRAW_FOUR:
                card_images.append(Image.open('Uno/assets/Wild_Draw.png', 'r'))
            elif card.value == Card.CARD_DRAW_TWO:
                card_images.append(Image.open(f'Uno/assets/{card.colour.capitalize()}_Draw.png', 'r'))
            else:
                card_images.append(Image.open(f'Uno/assets/{card.colour.capitalize()}_{card.value.capitalize()}.png', 'r'))
        return card_images
            
