from django.core.exceptions import ValidationError


def validate_exec(value):
    exec_values = ['canvas', 'underframe', 'molding']
    if value not in exec_values:
        raise ValidationError(
            'Неправильное значение исполнения',
            params={'value': value},
        )


def validate_order_status(value):
    order_status = ['processing', 'approved', 'paid', 'on da wey']
    if value not in order_status:
        raise ValidationError(
            'Неправильный статус заказа',
            params={'value': value}
        )