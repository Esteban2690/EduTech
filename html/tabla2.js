

    // Obtener los usuarios del backend
    fetch('http://localhost:4007/usuarios')
    .then(response => response.json())
    .then(usuarios => {
        const usuariosBody = document.getElementById('usuarios-body');
        usuarios.forEach(usuario => {
        // Crear una fila de la tabla por cada usuario
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${usuario.id_usuario}</td>
            <td>${usuario.nombre_usuario}</td>
            <td>${usuario.apellido_usuario}</td>
            <td>${usuario.tel_usuario}</td>
            <td>
            <button class="btn btn-danger btn-sm" data-id_usuario="${usuario.id_usuario}" onclick="eliminarUsuario(this)">Eliminar</button>
          </td>
        `;
        usuariosBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error:', error));

 //-----------------------------------------------------------------------------------------------------------------------------------   

   // Función para eliminar un usuario
function eliminarUsuario(button) {
    const idUsuario = button.dataset.id;
    fetch(`http://localhost:4007/usuarios/${idUsuario}`, {
      method: 'DELETE'
    })
    .then(response => {
      if (response.ok) {
        // Eliminar la fila de la tabla si la eliminación fue exitosa
        const row = button.closest('tr');
        row.remove();
        console.log(`Usuario con ID ${idUsuario} eliminado correctamente`);
      } else {
        console.error('Error al eliminar usuario:', response.status);
      }
    })
    .catch(error => console.error('Error:', error));
  }
