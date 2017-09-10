import libtcodpy as libtcod

from entity import Entity
from components.equipable import Equippable
from components.equipment import EquipmentSlots
from components.item import Item
from game_messages import Message
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from random_utils import random_choice_from_dict
from render_functions import RenderOrder


class ItemFactory:
    @staticmethod
    def get_item(item_dict, item_chances, entities, x, y):
        use_functions = {'heal': heal,
                         'cast_lightning': cast_lightning,
                         'cast_confuse': cast_confuse,
                         'cast_fireball': cast_fireball,
                         None: None
                         }
        slots = {'main_hand': EquipmentSlots.MAIN_HAND,
                 'off_hand': EquipmentSlots.OFF_HAND,
                 None:None}

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            item_choice = item_dict[random_choice_from_dict(item_chances)]

            color = getattr(libtcod, item_choice['color'], libtcod.white)
            item_component = None
            equippable_component = None
            targeting_message = None

            if item_choice.get('item'):
                use_function = use_functions.get(item_choice['item_use_parameters'].get('function'))
                amount = item_choice['item_use_parameters'].get('amount')
                targeting = item_choice['item_use_parameters'].get('targeting')
                message = item_choice['item_use_parameters'].get('message')
                if message:
                    message = Message(message,
                                      item_choice['item_use_parameters'].get('message_color'))
                if targeting:
                    targeting_message = message
                damage = item_choice['item_use_parameters'].get('damage')
                radius = item_choice['item_use_parameters'].get('radius')
                effect_range = item_choice['item_use_parameters'].get('range')

                item_component = Item(use_function=use_function,
                                      amount=amount,
                                      targeting=targeting,
                                      targeting_message=targeting_message,
                                      damage=damage,
                                      radius=radius,
                                      range=effect_range)
            if item_choice.get('equippable'):
                slot = slots.get(item_choice['equippable_parameters'].get('slot'))
                power_bonus = item_choice['equippable_parameters'].get('power_bonus')
                defense_bonus = item_choice['equippable_parameters'].get('defense_bonus')
                equippable_component = Equippable(slot,
                                                  power_bonus=power_bonus,
                                                  defense_bonus=defense_bonus)

            item = Entity(x, y, color=color,
                          char=item_choice['symbol'],
                          name=item_choice['name'],
                          render_order=RenderOrder.ITEM,
                          item=item_component,
                          count_value=1,
                          equippable=equippable_component)
            return item
