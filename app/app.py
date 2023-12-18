#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Validation functions
def validate_strength(strength):
    if not strength or not isinstance(strength, int):
        return False
    return True

def validate_description(description):
    if not description or len(description) > 255:  # Example: Max length of 255 characters
        return False
    return True

@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

@app.route('/heroes/<int:hero_id>')
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    else:
        abort(404, description='Hero not found')

@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def get_or_update_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        abort(404, description='Power not found')

    if request.method == 'GET':
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        response = make_response(jsonify(power_data), 200)
        response.headers['Custom-Header'] = 'Custom Value'
        return response

    if request.method == 'PATCH':
        data = request.json
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            updated_power_data = {'id': power.id, 'name': power.name, 'description': power.description}
            response = make_response(jsonify(updated_power_data), 200)
            response.headers['Custom-Header'] = 'Updated Custom Value'
            return response
        else:
            response = make_response(jsonify({'error': 'Invalid request'}), 400)
            response.headers['Custom-Header'] = 'Error Value'
            return response

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    # Validate input data
    if not hero_id or not power_id or not validate_strength(strength):
        abort(400, description='Invalid request')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        abort(404, description='Hero or Power not found')

    # Validate and create HeroPower
    if validate_description(power.description):
        hero_power = HeroPower(hero=hero, power=power, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

        hero_power_data = {
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength
        }

        response = make_response(jsonify(hero_power_data), 201)
        response.headers['Custom-Header'] = 'Created Custom Value'
        return response
    else:
        abort(400, description='Invalid request: Description validation failed')

if __name__ == '__main__':
    app.run(port=5555)





















# from flask import Flask, jsonify, abort, request, make_response
# from models import db, Hero, Power
# from flask_migrate import Migrate


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/heroes')
# def get_heroes():
#     heroes = Hero.query.all()
#     heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
#     return jsonify(heroes_data)

# @app.route('/heroes/<int:hero_id>')
# def get_hero(hero_id):
#     hero = Hero.query.get(hero_id)
#     if hero:
#         hero_data = {
#             'id': hero.id,
#             'name': hero.name,
#             'super_name': hero.super_name,
#             'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
#         }
#         return jsonify(hero_data)
#     else:
#         abort(404, description='Hero not found')

# @app.route('/powers')
# def get_powers():
#     powers = Power.query.all()
#     powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
#     return jsonify(powers_data)

# @app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
# def get_or_update_power(power_id):
#     power = Power.query.get(power_id)
#     if not power:
#         abort(404, description='Power not found')

#     if request.method == 'GET':
#         power_data = {'id': power.id, 'name': power.name, 'description': power.description}
#         return jsonify(power_data)

#     if request.method == 'PATCH':
#         data = request.json
#         if 'description' in data:
#             power.description = data['description']
#             db.session.commit()
#             return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
#         else:
#             abort(400, description='Invalid request')


# if __name__ == '__main__':
#     app.run(port=5555)
