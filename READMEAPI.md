# VotacionesM4

VotacionesM4 es una aplicación web que te permite crear y votar en encuestas personalizadas , comentarlas y compartir la experiencia.

## Características

- Vota en las encuestas creadas por otros usuarios.
- Comenta y comparte tus opiniones sobre las preguntas.
- Reporta contenido inapropiado.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/decide.git

## Funcionalidades

1. Accedemos a la vista principal de la aplicación, como usuario no autenticado:
   Tenemos acceso a loguearnos, registrarnos, y cambiar el idioma. Además de poder acceder a las urls del footer.
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/inicio.png?raw=true)

2. Nos registramos como usuario nuevo, pulsando el botón de registrarse, rellenamos los campos.
   La contraseña debe cumplir con los requisitos establecidos y no ser muy similar al nombre de usuario. El email debe cumplir el formato.
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/signin.png?raw=true)

2.1. En caso de contar con una cuenta ya, podemos acceder mediante el botón de iniciar sesión.
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/login.png?raw=true)

2.2 Además, podemos inciar sesión con google.
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/google_1.png?raw=true)

   Pulsamos el boton de continuar y nos solicita acceso desde google a nuestra cuenta personal para acceder a la aplicacion.


3. Accedemos a la vista principal como usuario autenticado.
   Aquí vemos que hay nuevas funcionalidades una vez autenticados.
    ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/inicio_auth.png?raw=true)

4. Podemos cambiar de idioma, a francés, inglés o español.
    ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/idiomas.png?raw=true)
    ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/ingles.png?raw=true)
    ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/frances.png?raw=true)

5. Podemos también, crear una votación:
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/create_voting.png?raw=true)

6. Una vez creada, deberiamos acceder a localhost:8000/admin, crear un censo referente a esa votación, e inicializarla.
   Una vez completado este proceso, accedemos a votaciones asignadas:
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/votaciones_asignadas.png?raw=true)

7. Accedemos a una votación que tengamos asignada, pulsando en su id, y realizamos el voto.
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/booth_single_kent.png?raw=true)

8. Volvemos a inicio, podemos acceder ahora a las votaciones finalizadas:
   En esta vista, podemos ver la lista de votaciones finalizadas y una lista de comentarios.
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/votaciones_finalizadas.png?raw=true)
   
   Los comentarios se pueden crear, borrar, editar, o reportar.
   Tienes 5 minutos despues de la creacion de un comentario para poder borrar o editar este, sino, estas acciones no seran permitidas:
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/no_permitido_comentarios.png?raw=true)

   Se pueden borrar y editar siempre que sean tuyos.
   Al crear un comentario, su autor es el usuario con el que esta autenticado que haya creado dicho comentario, lo cual se asigna automaticamente.
   Vamos a analizar como ver los resultados de una votacion finalizada
   Para finalizar una votación, antes ha debido ser acabada y realizado el conteo mediante localhost:8000/admin
   

10. Accedemos a una votacion finalizada mediante su ID y vemos los datos guardados sobre esta.
    ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/visualizer.png?raw=true)

11. Volvemos a inicio y volvemos a acceder a votaciones finalizadas, ahora, podemos comentar sobre que nos han parecido las preguntas o la votacion.
    Accedemos a esto mediante el boton de agregar comentario:
    ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/agregar_comentario.png?raw=true)

    Hay que tener cuidado con las palabras que se utilizan, ya que esta vista consta con un filtro de badwords, en donde se advertirá del uso de malas palabras, pero se permitirá, aun asi, añadir los comentarios, pero cuentan con la posibilidad de ser posteriormente reportados.

   También, como comentamos antes, se pueden borrar, editar y reportar comentarios, siempre que estemos en el plazo permitido de 5 minutos tras su creacion:
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/editar_comentario.png?raw=true)
   ![image](https://github.com/decide-single-kent/decide-single-kent/blob/feature/72-Complete_documentation/resources/reportar_comentario.png?raw=true)

12. Finalmente podemos cerrar sesión y volver a la pagina de inicio de usuario no autenticado.
   








   

