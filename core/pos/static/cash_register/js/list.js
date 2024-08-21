var tblCashRegister;

var cash_register = {
    list: function () {
        tblCashRegister = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search'
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "user.username"},
                {"data": "opening_date"},
                {"data": "closing_date"},
                {"data": "initial_amount"},
                {"data": "current_amount"},
                {"data": "final_amount"},
                {"data": "active"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-6, -7],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.active) {
                            return '$' + data.toFixed(2);
                        }
                        return '---';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (typeof data === 'number') {
                            return '$' + data.toFixed(2);
                        }
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-pill badge-success">Activo</span>';
                        }
                        return '<span class="badge badge-pill badge-danger">Inactivo</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '';
                        if (row.active) {
                            buttons += '<a rel="finish" data-toggle="tooltip" title="Cerrar caja" class="btn btn-secondary btn-xs btn-flat"><i class="fas fa-hand-holding-usd"></i></a> ';
                            buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        }
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    cash_register.list();

    $('#data tbody')
        .off()
        .on('click', 'a[rel="finish"]', function () {
            $('.tooltip').remove();
            var tr = tblCashRegister.cell($(this).closest('td, li')).index(),
                row = tblCashRegister.row(tr.row).data();
            var params = new FormData();
            params.append('action', 'finish_cash_register');
            params.append('id', row.id);
            var args = {
                'params': params,
                'content': '¿Estas seguro de cerrar la siguiente caja?',
                'success': function (request) {
                    alert_sweetalert({
                        'message': 'Se ha cerrado correctamente la caja',
                        'timer': 2500,
                        'callback': function () {
                            tblCashRegister.ajax.reload();
                        }
                    })
                }
            };
            submit_with_formdata(args);
        });
});