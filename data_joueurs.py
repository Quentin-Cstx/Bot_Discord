# database.py
import sqlite3

class Database:
    def __init__(self, db_file='player_database.db'):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.init_tables()
    
    def init_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            name TEXT PRIMARY KEY,
            level INTEGER NOT NULL,
            experience INTEGER DEFAULT 0
        )
        ''')
        self.connection.commit()
    
    def add_player(self, name, level):
        if not name or not isinstance(level, int):
            raise ValueError("Name must be a non-empty string and level must be an integer.")
        self.cursor.execute('INSERT INTO players (name, level) VALUES (?, ?)', (name, level))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_player(self, player_name):
        self.cursor.execute('SELECT * FROM players WHERE name = ?', (player_name,))
        return self.cursor.fetchone()

    def increment_player_level(self, player_name, increment=1):
        self.cursor.execute('UPDATE players SET level = level + ? WHERE name = ?', (increment, player_name))
        self.connection.commit()
        return self.cursor.rowcount
    
    def add_experience(self, player_name, experience):
        if not isinstance(experience, int) or experience < 0:
            raise ValueError("Experience must be a non-negative integer.")
        
        current_exp = self.get_experience(player_name)
        current_level = self.level_from_exp(current_exp)
        exp_needed = self.exp_for_level(current_level + 1)
        while current_exp + experience >= exp_needed:
            experience -= (exp_needed - current_exp)
            current_level += 1
            self.increment_player_level(player_name)
            current_exp = 0
            exp_needed = self.exp_for_level(current_level + 1)
        self.cursor.execute('UPDATE players SET experience = experience + ? WHERE name = ?', (experience, player_name))
        self.connection.commit()
        return self.cursor.rowcount
    
    def get_experience(self, player_name):
        self.cursor.execute('SELECT experience FROM players WHERE name = ?', (player_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def delete_player(self, player_name):
        self.cursor.execute('DELETE FROM players WHERE name = ?', (player_name,))
        self.connection.commit()
        return self.cursor.rowcount
    
    def reset_database(self):
        """Supprime toutes les tables et les recrée"""
        self.cursor.execute('DROP TABLE IF EXISTS players')
        self.connection.commit()
        self.connection.close()
        self.connection = sqlite3.connect('player_database.db')
        self.cursor = self.connection.cursor()
        self.init_tables()
        print("Base de données réinitialisée")

    @staticmethod
    def exp_for_level(level):
        """Calcule l'XP nécessaire pour un niveau donné"""
        return 5 * (level ** 2) + 50 * level + 100
    
    @staticmethod
    def level_from_exp(exp):
        """Calcule le niveau à partir de l'XP totale"""
        level = 0
        while exp >= Database.exp_for_level(level + 1):
            level += 1
        return level
    

