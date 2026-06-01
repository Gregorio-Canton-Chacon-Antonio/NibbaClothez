# Documentación de aplicación
## 1 Objetivo
El propósito del proyecto es desarrollar una tienda virtual, donde los usuarios puedan comprar y vender productos de manera sencilla y rápida. La aplicación contará con funciones que permitan una gran comodidad en la búsqueda o venta, enfocándose en ofrecer una experiencia simple y fácil de usar pero aún así buena y confiable.

El alcance del proyecto incluye el registro de usuarios, publicación de productos, búsqueda por categorías, visualización de artículos y comunicación  entre compradores y vendedores. Será para todo tipo de usuarios sin restricciones en la ropa y con libertad en las descripciones y precios, todo lo que puede abarcar un estilo tendremos un espacio para todos, desde ropa deportiva hasta elegante buscamos ser una tienda con buena imagen donde cualquier tipo de persona se interese en comprar, que no parezca un sitio barato y de remate.

Las entidades que intervienen en el flujo de información son los usuarios compradores, los vendedores, la base de datos de productos y el sistema de la plataforma, encargado de almacenar, procesar y mostrar la información relacionada con las publicaciones, compras y cuentas de usuario.

Además, el sistema permitirá mantener un control organizado de los productos publicados, facilitando la búsqueda para usuarios y la recomendación y descripción para vendedores con etiqueta y descripciones, mejorando la experiencia de navegación de los usuarios. La plataforma estará enfocada en ser intuitiva, rápida y accesible, permitiendo que las personas puedan interactuar de manera sencilla al momento de comprar o vender artículos. 

Finalmente, el proyecto busca ofrecer una alternativa práctica para la compra y venta de productos en línea, promoviendo una comunicación eficiente entre usuarios y una administración adecuada de la información dentro del sistema para que encuentres todo en un solo sitio.

### 2 Registro
El proceso de registro permite a nuevos usuarios crear una cuenta en la plataforma. Para registrarse, el usuario debe proporcionar los siguientes datos:

- **Nombre completo**
- **Correo electrónico**
- **Contraseña**

Una vez el formulario esta lleno, el sistema valida que el correo no esté registrado anteriormente y que la contraseña cumpla con los requisitos mínimos de seguridad, al igual el correo electronico necesita cumplir los requisitos. Si todo es correcto, la cuenta es creada y el usuario puede iniciar sesión. una vez iniciada debe enviarte de nuevo a la pagina de inicio.

### 3 Login
El inicio de sesión permite a los usuarios registrados acceder a su cuenta. El usuario debe ingresar:

- **Correo electrónico**
- **Contraseña**

El sistema verifica que los datos sean correctos. Si los datos son válidos, el usuario es redirigido a la página principal de la tienda. En caso de error, se muestra un mensaje indicando que el correo o la contraseña son incorrectos. de igual manera aparece si la contraseña es valida.

### 4 Recuperación de Contraseña
En caso de que el usuario olvide su contraseña, la plataforma ofrece un proceso de recuperación:

1. El usuario ingresa su correo electrónico registrado.
2. El sistema envía un enlace de recuperación al correo.
3. El usuario accede al enlace y establece una nueva contraseña.
4. Una vez confirmada, puede iniciar sesión con la nueva contraseña.

### 5 Gestión de Productos (CRUD)

La plataforma contará con un sistema de gestión de productos que permitirá a los vendedores administrar sus publicaciones de manera sencilla. Este módulo incluirá las funciones básicas de un CRUD (Crear, Leer, Actualizar y Eliminar).

### Agregar productos
Los usuarios vendedores podrán publicar nuevas prendas ingresando información como:

- Nombre del producto.
- Descripción.
- Precio.
- Categoría.
- Imágenes del producto.

Una vez completados los datos, el sistema guardará la publicación y la mostrará dentro de la tienda para que otros usuarios puedan visualizarla. pero lo importante es que tu puedes verlas en tu perfil editarlas, borrarlas.

### Editar productos
Los vendedores podrán modificar la información de sus publicaciones en cualquier momento. El sistema permitirá actualizar datos como el nombre, descripción, precio, categoría o imágenes del producto.

### Eliminar productos
Los vendedores también tendrán la opción de eliminar publicaciones que ya no deseen mostrar en la plataforma. Una vez eliminada la prenda, dejará de aparecer en la tienda y no podrá ser visualizada por otros usuarios.

### Visualización de productos
Los productos publicados podrán ser visualizados por todos los usuarios dentro de la plataforma, mostrando la información y detalles proporcionados por el vendedor.

### 6 Diseño de Interfaz

La plataforma contará con una interfaz moderna, sencilla e intuitiva, diseñada para facilitar la navegación y mejorar la experiencia de los usuarios al comprar o vender productos. El diseño estará enfocado en la claridad visual, el acceso rápido a las funciones principales y la adaptación a diferentes dispositivos.

### Página de Inicio
La página principal mostrará los productos destacados y las publicaciones más recientes. También contará con una barra de búsqueda y opciones para filtrar productos por categorías. Desde esta pantalla los usuarios podrán acceder al inicio de sesión, registro y perfil personal.

### Página de Registro e Inicio de Sesión
Las pantallas de registro y acceso presentarán formularios simples y fáciles de completar. Los usuarios podrán crear una cuenta, iniciar sesión o acceder a la opción de recuperación de contraseña desde una misma sección.

### Perfil de Usuario
Cada usuario dispondrá de un perfil donde podrá visualizar y administrar sus publicaciones. Desde esta sección será posible agregar nuevos productos, editar publicaciones existentes o eliminar aquellas que ya no deseen mostrar.

### Catálogo de Productos
El catálogo permitirá visualizar todos los artículos disponibles en la plataforma mediante tarjetas que mostrarán la imagen, nombre, precio y categoría del producto. Los usuarios podrán seleccionar cualquier artículo para consultar información más detallada.

### Vista de Producto
Al acceder a un producto, se mostrará una página con información completa sobre la publicación, incluyendo imágenes, descripción, precio y datos del vendedor. Esta vista permitirá al usuario conocer mejor el artículo antes de realizar una compra o contactar al vendedor.

### Diseño Responsive
La interfaz estará diseñada para adaptarse correctamente a computadoras, tabletas y teléfonos móviles, garantizando una experiencia de navegación cómoda y consistente en diferentes tamaños de pantalla.

##  Integrantes

### Integrante 1
- **Nombre Completo:** Gregorio Canton Chacon Antonio

<img width="200" height="202" alt="integrante1" src="https://github.com/user-attachments/assets/f6a87c43-2190-47cb-bf01-ae8cf94b9d7e" />

 ### Integrante 2
- **Nombre Completo:** Herrera Trejo Victor Daniel

<img width="200" height="202" alt="integrante2" src="https://github.com/user-attachments/assets/e27750c8-92a3-4d30-9f5f-fdd2d3be4220" />
