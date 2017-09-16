import libtcodpy as libtcod
from components.equipable import Equippable
from components.equipment import EquipmentSlots
from components.item import Item
from entity import Entity
from game_messages import Message
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from random_utils import random_choice_from_dict
from render_functions import RenderOrder


class ItemFactory:
    use_functions = {'heal': heal,
                     'cast_lightning': cast_lightning,
                     'cast_confuse': cast_confuse,
                     'cast_fireball': cast_fireball,
                     None: None
                     }
    slots = {'main_hand': EquipmentSlots.MAIN_HAND,
             'off_hand': EquipmentSlots.OFF_HAND,
             None: None}

    @staticmethod
    def get_item(item_dict, item_chances, entities, x, y):
        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            return ItemFactory.get_item_by_name(item_dict,
                                                random_choice_from_dict(item_chances),
                                                x, y)

    @staticmethod
    def get_item_by_name(item_dict, item_name, x, y):
        item_choice = item_dict[item_name]

        color = getattr(libtcod, item_choice['color'], libtcod.white)
        item_component = None
        equippable_component = None
        targeting_message = None
        treasure_value = item_choice.get('treasure_value', 0)

        if item_choice.get('item'):
            use_function = ItemFactory.use_functions.get(item_choice['item_parameters'].get('function'))
            amount = item_choice['item_parameters'].get('amount')
            targeting = item_choice['item_parameters'].get('targeting')
            is_treasure = item_choice['item_parameters'].get('is_treasure', False)
            message = item_choice['item_parameters'].get('message')
            if message:
                message = Message(message,
                                  item_choice['item_parameters'].get('message_color'))
            if targeting:
                targeting_message = message
            damage = item_choice['item_parameters'].get('damage')
            radius = item_choice['item_parameters'].get('radius')
            effect_range = item_choice['item_parameters'].get('range')

            item_component = Item(use_function=use_function,
                                  amount=amount,
                                  is_treasure=is_treasure,
                                  targeting=targeting,
                                  targeting_message=targeting_message,
                                  damage=damage,
                                  radius=radius,
                                  range=effect_range)
        if item_choice.get('equippable'):
            slot = ItemFactory.slots.get(item_choice['equippable_parameters'].get('slot'))
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
                      treasure_value=treasure_value,
                      equippable=equippable_component)
        return item
    
    @staticmethod
    def build_item(x, y, item_color='white', item_symbol='.', item_name='Generic Item',
                   treasure_value=0,
                   is_item=False, item_parameters=None,
                   is_equippable=False, equippable_parameters=None):

        color = getattr(libtcod, item_color, libtcod.white)
        item_component = None
        equippable_component = None
        targeting_message = None
        treasure_value = treasure_value

        if is_item:
            use_function = ItemFactory.use_functions.get(item_parameters.get('function'))
            amount = item_parameters.get('amount')
            targeting = item_parameters.get('targeting')
            is_treasure = item_parameters.get('is_treasure', False)
            message = item_parameters.get('message')
            if message:
                message = Message(message,
                                  item_parameters.get('message_color'))
            if targeting:
                targeting_message = message
            damage = item_parameters.get('damage')
            radius = item_parameters.get('radius')
            effect_range = item_parameters.get('range')

            item_component = Item(use_function=use_function,
                                  amount=amount,
                                  is_treasure=is_treasure,
                                  targeting=targeting,
                                  targeting_message=targeting_message,
                                  damage=damage,
                                  radius=radius,
                                  range=effect_range)
        if is_equippable:
            slot = ItemFactory.slots.get(equippable_parameters.get('slot'))
            power_bonus = equippable_parameters.get('power_bonus')
            defense_bonus = equippable_parameters.get('defense_bonus')
            equippable_component = Equippable(slot,
                                              power_bonus=power_bonus,
                                              defense_bonus=defense_bonus)

        item = Entity(x, y, color=color,
                      char=item_symbol,
                      name=item_name,
                      render_order=RenderOrder.ITEM,
                      item=item_component,
                      count_value=1,
                      treasure_value=treasure_value,
                      equippable=equippable_component)
        return item
