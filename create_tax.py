#!/usr/bin/env python3
import sys
import os

# Add Odoo to Python path
sys.path.append(r'C:\Odoo18\odoo')

import odoo

# Parse config
config_file = r'C:\Odoo18\odoo.conf'
odoo.tools.config.parse_config(['-c', config_file])

# Initialize Odoo
odoo.modules.initialize_sys_path()
odoo.netsvc.init_logger()

# Get database name
db_name = odoo.tools.config['db_name']

# Connect to database
registry = odoo.registry(db_name)
with registry.cursor() as cr:
    # Create environment
    uid = odoo.SUPERUSER_ID
    env = odoo.api.Environment(cr, uid, {})
    
    print("Setting up Romanat Hotel System...")
    
    # 1. Create accounts if needed
    income_account = env['account.account'].search([
        ('name', 'ilike', 'service charge'),
        ('account_type', '=', 'income')
    ], limit=1)
    
    if not income_account:
        income_account = env['account.account'].create({
            'name': 'Hotel Service Charge Income',
            'code': '411200',
            'account_type': 'income',
        })
        print(f"✓ Created account: {income_account.name}")
    
    liability_account = env['account.account'].search([
        ('name', 'ilike', 'tips'),
        ('account_type', '=', 'liability_current')
    ], limit=1)
    
    if not liability_account:
        liability_account = env['account.account'].create({
            'name': 'Waiter Tips Payable',
            'code': '224200',
            'account_type': 'liability_current',
        })
        print(f"✓ Created account: {liability_account.name}")
    
    # 2. Create service charge tax
    tax = env['account.tax'].create({
        'name': 'Service Charge 10%',
        'amount': 10.0,
        'amount_type': 'percent',
        'type_tax_use': 'sale',
        'price_include': False,
        'invoice_repartition_line_ids': [
            (0, 0, {'repartition_type': 'base'}),
            (0, 0, {'repartition_type': 'tax', 'factor': 0.5, 'account_id': liability_account.id}),
            (0, 0, {'repartition_type': 'tax', 'factor': 0.5, 'account_id': income_account.id}),
        ],
    })
    print(f"✓ Created tax: {tax.name}")
    
    # 3. Create POS product
    product = env['product.product'].create({
        'name': 'Meat Plate',
        'type': 'consu',
        'list_price': 100,
        'available_in_pos': True,
        'taxes_id': [(6, 0, [tax.id])],
    })
    print(f"✓ Created product: {product.name}")
    
    # 4. Create room product
    room_product = env['product.product'].create({
        'name': 'Standard Room',
        'type': 'service',
        'list_price': 3000,
        'available_in_pos': False,
    })
    print(f"✓ Created room product: {room_product.name}")
    
    # 5. Create POS config
    pos_config = env['pos.config'].search([('name', 'ilike', 'hotel')], limit=1)
    if not pos_config:
        pos_config = env['pos.config'].create({
            'name': 'Hotel Restaurant POS',
            'module_pos_hr': True,
            'is_restaurant': True,
        })
        print(f"✓ Created POS config: {pos_config.name}")
    
    # 6. Create room type and room
    room_type = env['hotel.room.type'].create({
        'name': 'Standard',
        'product_id': room_product.id,
    })
    
    room = env['hotel.room'].create({
        'name': '101',
        'room_type_id': room_type.id,
        'state': 'available',
        'housekeeping_state': 'clean',
    })
    print(f"✓ Created room: {room.name}")
    
    # 7. Create waiter
    employee = env['hr.employee'].create({
        'name': 'Waiter 1',
        'work_email': 'waiter1@romanat.com',
    })
    print(f"✓ Created employee: {employee.name}")
    
    cr.commit()
    print("\n✅ Setup completed successfully!")