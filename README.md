# Explicación Tarea 5

## Santiago Muñoz Venezian; santi95

11 de Noviembre, 2017

Para que sea más facil de corregir, lo que no me funcionó fue:

    1. Los Choques entre monstruos no funcionan bien, se atraviesan
    2. Hice un commit a las 12:10, 10 minutos luego de la hora de entrega con todas las ventanas
    estilizadas. No alcancé antes! :( el fondo se me estaba agregando a todos los widgets, pero
    aprendí a hacerlo a último minuto y morí.
    3. El safe zone hace que no me ataquen, pero al esconder al personaje principal me tira un error
    4. El draggable de la tienda, funciona, pero si arrastrar los qwidgets

Todo el resto funciona super bien en general

Mi tarea tiene 9 archivos.

    1. FrontEnd
    2. BackEnd
    3. BackEndTienda
    4. constantes
    5. FuncioneUtiles
    6. character.ui  #Al final no fue usado
    7. Game.ui
    8. Main.ui
    9. Tienda.ui

#### 1. FrontEnd

1. Se importa todo lo necesario.

2. creamos las interfaces creados por QTDesigner

3. class MainWindow:

    Al iniciarse intenta leer un archivo de highscores, sino lo crea.

    Tiene un fondo de pantalla acorde a la temática del juego.

    Tiene un boton que abre el juego y esconde la pantalla principal

4. class DropBox y DraggableLabel:

    Lo saque de stackoverflow, intenté hacer la tienda con el botón Draggable, pero
    alfinal decidí hacerla con botones de aumentar y disminuir ya que no me funcionaba

5. Store:

    Importa todo de la interfaz creada en QTDesigner de el archivo Tienda.ui

    La tienda es ajustable de tamaño y no pierde su cuadratura al hacerle cambios.

    No me funcionó hacer los botones draggables, pero la tienda está 100% funcional,
    cumple todas las funciones de la tienda y quedó horrible en el commit de las 11:59,
    pero en el de 10 minutos después pude hacer el fondo temático, con el mismo diseño
    de el resto del juego.

    Las funciones abajo, ajustan la interfaz gráfica del juego una vez que se relizan los cabios.
    También hacen que personaje principal tenga los cambios pedidos en la tienda.

    Lo comentado del final, son las variables creadas para el draggable, que no entiendo
    porque no me funcionaron :(

6. class Game:

    Importa la interfaz desde el archivo Game.ui

    Le creamos un fondo acorde a la temática del juego y setemamos los puntajes que
    se van a mostrar al inicio del juego. No se cumple pep8 en el init, pero se
    entiende mejor que es lo que se hace.

    Tenemos un botón de pausa total, uno de tienda y uno de salir que genera un gameover().
    En la linea 240, se setea la geometría inicial del juego y se le dá el título a la ventana.
    'Mejor que LOL', se setea el nivel inicial, y la barra de avance en 0.

    Generamos el alto y ancho de el window, para despúes agregar los demás Widgets a un
    tamaño adecuado y a los personajes dentro de el window.

    Se crea el personaje principal y se inicia su thread

    def time: Le entrega al front end los eventos que pasan de acuerdo a una distribución de tiempo.
    Se encarga además de la creación de enemigos y la de eventos extras, como la vida extra.

    Se tiene una property del puntaje, para que siempre que este se cambie, setee la interfaz
    gráfica.

    Property del avance de la barra de nivel, Este hace que el personaje crezca en la interfaz
    cada vez que se completa el 50% de la barra, o cada vez que se sube de nivel.
    Además cambia el tamaño de la barra de nivel en la interfaz cada ves que el avance cambia durante
    el juego. Es el responsable también de que se acabe el juego cuando se llega al 100%
    de la barra del nivel 5 dentro de otras cosas, como el puntaje extra que se gana
    cada vez que se sube de nivel.

    Hay 4 StaticMethods que se llaman con triggers desde el backend.
    El de actualizar_imagen hace que los personajes se muevan cuando hay un cambio de posicion,
    el de agrandar_imagen se encarga de que la imagen crezca a partir de otro trigger,
    el de atacar, que se encarga de bajarle la vida al personaje atacado y finalmente,
    el de Bonuses que son los que se encargan de las funcionalidades de cada uno de los eventos
    creados.

    Desde la linea 421 hasta la linea 458 se procesan las teclas, se pueden apretar simultaneamante.

    La letra C es un cheat para que el personaje principal crezca.

    Las lestras 'W A S D' hacen que el personaje se mueva

    La letra F, convierte la pantalla de juego en FullScreen

    Las combinaciones ctrl S y ctrl T, respectivamente pausan el juego y abren la tienda

    Luego están las funciones de abrir la tienda, la pauda total y el gameover()

        a. Abrir la tienda le entrega al window tienda, los bonus actuales y muestra
        la tienda sin cerrar el juego

        b. La pausa_total, pone el juego en pausa y muestra el QLabel pausa ocultado
        en el init del esta clase, con una posición nueva que depende del tamaño actual
        de la ventana.

        c. game_over, actualiza el Highscores.txt si es que puede, osino lo crea.
        Mata a todos los personjes en juego, espera 4 segundos a que pase la animación
        y muestra el Main nuevamente.

#### 2. Backend

1. class MoveMyImageEvent:

    El objeto que le entregamos con un trigger al abstract method actualizar_imagen.

2. class ChangeSizeEvent

    El objeto que le entregamos con un triger al abstractmethod de agrandar_imagen

3. class Atacar

    El objeto que le entregamos con un triger al abstractmethod de atacar

4. class Dino

    Parte con los 4 triggers y una lista de todos los objetos activos dentro del juego.

    Hay tantos elementos en común entre los enemigos y el personaje principal que decidí
    hacer una sola clase para ambos.

    Dependiendo del self.foto que se le entregue, se crean distintos atributos que necesitan
    cada uno de los personajes.
    Inicialmente iba a crear todos los personajes con un character.ui, pero decidí no hacerlo.

    En el init se setean todos los atributos de los personjes, se les entrega su imagen
    y su progressbar arriba de la cabeza.

    Se les dá un id tamaño, que bonuses tienen, vida maxima y actual con un property,
    una velocidad de movimiento y otra de ataque. se setea la foto inicial de la animación
    con una tupla y se asocia a un property para animarlos eficientemente.

    Se crea el Pixmap para entregarle al objeto, se conectan los triggers, se les dá una posición
    y por ultimo se les calcula el centro de la imagen. Además se crea el próximo tiempo
    en el cual se va a crear un enemigo.

    Property Vida: Les da su estado self.muerto cuando su vida es menor a 0,
    el self.muerto mata el thread y llama a funciones explicadas más adelante.

    Property Position: Hace que los personajes choquen siempre con el borde, independientemente
    del tamaño de la ventana elegida. Cada vez que el un mono se mueve, toma el tamaño de la ventana
    y lo deja moverse con respecto a ella.

    Property Size: Llama al sizetrigger, que hace que crezca en el FrontEnd

    Property nro_foto: Se encarga de que las animaciones se muevan sin problema, estámn seteadas
    para que funcionen las de ataque, pero el tiempo se me hizo poco.

    def crece: Calcula nueva vida máxima, nuevo ataque y cambia el tamaño de la progressBar de vida

    def calcular_zona: Crea un circulo alrededor del personaje que si alguien más entra en él,
    se produce un choque.

    def check_dir: Revisa las teclas apretadas y cambia el position, que el property
    hace que se vea en la interfaz. Al final hace que el personaje esté animado.

    def check_crash: se ven 3 tipos de ataques, usuario malo, usuario extra, malo, usuario.
    Hacen atacktriggers y bonustriggers que llaman a lo que tiene que pasar cuando chocan con algo.
    Tambiémn revisa si esque el personaje no está en el safezone.

    def malo_moverse: Hace que los personajes malvados se muevan dependiendo de la posición
    de la posición del personaje principal. Además anima el movimiento de los malos, mientras
    que están o escapando o en una persecución.

    Finalmente el run: Revisa si está muerto o no, espera el tiempo de la velocidad del personaje.


    Tiene un contador, que por ejemplo, si el personaje se mueve a 0.1 segundos y ataca cada
    1 segundo, cada posibles movimientos, el personaje ataca. Esto se acgtualiza cada vez que
    la tienda es usada.

    Además esconde al personaje cada vez que aparece un safezone, pero eso
    tira un error que no pude solucionar.

    Hace que se anime el personaje con su caminara normal.

    Si se muere el Thread, muerto = True, se hace la animación de la muerte y se escodne el personaje.

    5. class Extras: Eran threads, pero el programa se ponía lento, por lo tanto
    alfinal solamente fueron QLabels. Tienen elementos parecidos a los personajes,
    la foto, el estado muerto, un radio de choque y una imagen para que los choques funcionen
    adecuadamente.





#### 3. BackendTienda

    Tiene una clase de FuncionalidadTienda, que le entrego todo o que le interesa a la tienda
    acerca del juego. Luego tiene una función que trabaja con eso y chequea que se cumplan las
    condicionesdel enunciado acerca de la tienda.


#### 4. constantes

    Las lee para las condiciones iniciales del juego

#### 5. FuncionesUtiles

    def distancia: Nos entrega la distancia entre los centros de 2 objetos, usada para los choques.

    def prox_apar: Le da al FrontEnd el tiempo en el cual tiene que crear
    un enemigo extra del juego

    def prox_extra: Le entrega al FrontEnd el tiempo en el cual tiene que crear cierto elemento extra,
    saque el safezone para probar algo, pero luego se me olvidó ponerlo de vuelta! sorryy!

    def retornar_tamano: le dice al frontEnd cual tiene que se el tamaño del nuevo
    malo creado por el juego.

#### 6. Designer

    Los archivos del 6 al 9 son .ui, son layouts que cree para que el juego al ser agrandado
    no pierda su forma. Algunos elementos fueron creados para ser ocultados en un init y mostrados
    cuando necesarios, como por ejemplo el Pausa del Game o el Game Over.


--------------------------------------------------------------------------------------------


Bacan la Tarea! Espero que este ReadMe te haya servido con este fin de semestre.
Entretenida la Tarea!! Por el resto de mis ramos no pude dedicarle todo el tiempo que quise,
pero Gracias por corregirmela!!! :D

