    document.getElementById('barra-busqueda').addEventListener('input', function () {
        const query = this.value.trim();

        if (query.length > 0) {
            fetch(`?q=${query}`)  // Realiza la búsqueda usando la misma vista de listado
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const nuevosProductos = doc.querySelector('#lista-productos').innerHTML;

                    document.getElementById('lista-productos').innerHTML = nuevosProductos;
                })
                .catch(error => console.error('Error al buscar productos:', error));
        } else {
            location.reload(); // Recargar la página si el campo está vacío
        }
    });

const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})