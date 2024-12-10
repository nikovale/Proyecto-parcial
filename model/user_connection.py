import psycopg # type: ignore

class UserConnection:
    Conn = None

    def __init__(self):
        try:
          self.conn = psycopg.connect("dbname='Proyecto-parcial' user='postgres' password='2343' host='localhost' port='5432'")
        except psycopg.operationalError as err:
             print("Error: ", err)
             self.conn.close()

    def read_all(self):
        with self.conn.cursor() as cur:
            data = cur.execute("""
             SELECT * FROM "users"
            """)
            return data.fetchall()
    
    def read_one(self, id):
        with self.conn.cursor() as cur:
            data=cur.execute("""
             SELECT * FROM "users" WHERE id = %s
            """, (id,))
            return data.fetchone()

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""INSERT INTO
                        "users"(full_name, password, correo) VALUES(%(full_name)s, %(password)s, %(correo)s)
                        """,data )
            self.conn.commit()
        
    def update(self, data):
        with self.conn.cursor() as cur:
           cur.execute("""
                    UPDATE "users" SET full_name = %(full_name)s,
                            phone = %(phone)s WHERE id= %(id)s
                    """, data)
           self.conn.commit()
        
    def delete(self, id):
        with self.conn.cursor() as cur:
           cur.execute("""
              DELETE FROM "users" WHERE id = %s
           """, (id,))
           self.conn.commit()

    def read_by_email_and_password(self, correo, password):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM "users" WHERE correo = %s AND password = %s
                """, (correo, password))
                data = cur.fetchone()
                if data:
                    return {
                        "id": data[0],
                        "full_name": data[1],
                        "password": data[2],
                        "correo": data[3]
                    }
                return None  # Si no se encuentra, devolver None
        except psycopg.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return None

    def __def__(self):
        self.conn.close()