import sys
import os

# Add Odoo to path
sys.path.append(r'C:\Odoo18\odoo')

# Initialize Odoo
import odoo

# Parse config
odoo.tools.config.parse_config(['-c', r'C:\Odoo18\odoo.conf', '-d', 'odoo'])

# Start Odoo services
odoo.service.db._create_empty_database('odoo')
odoo.netsvc.init_logger()
odoo.modules.initialize_sys_path()

# Import required modules
from odoo.modules.registry import Registry

# Get registry
registry = Registry('odoo')

with registry.cursor() as cr:
    # Create environment
    uid = odoo.SUPERUSER_ID
    env = odoo.api.Environment(cr, uid, {})
    
    print("=" * 60)
    print("STARTING ROMANAT HOTEL SETUP")
    print("=" * 60)
    
    # Get company
    company = env.company
    print(f"Working with company: {company.name}")
    
    # 1. Install chart of accounts if needed
    if not company.chart_template:
        print("\n1. Installing Chart of Accounts...")
        template = env['account.chart.template'].search([], limit=1)
        if template:
            template.try_loading(company=company)
            print("   ✓ Chart installed")
    
    # 2. Create accounts
    print("\n2. Creating accounts...")
    income_account = env['account.account'].create({
        'name': 'Hotel Service Charge Income',
        'code': '411200',
        'account_type': 'income',
        'company_id': company.id,
    })
    print(f"   ✓ {income_account.code} - {income_account.name}")
    
    liability_account = env['account.account'].create({
        'name': 'Waiter Tips Payable',
        'code': '224200',
        'account_type': 'liability_current',
        'company_id': company.id,
    })
    print(f"   ✓ {liability_account.code} - {liability_account.name}")
    
    # 3. Create tax
    print("\n3. Creating service charge tax...")
    tax = env['account.tax'].create({
        'name': 'Service Charge 10%',
        'amount': 10.0,
        'amount_type': 'percent',
        'type_tax_use': 'sale',
        'price_include': False,
        'company_id': company.id,
        'description': '5% service + 5% tips',
    })
    print(f"   ✓ {tax.name}")
    
    # Set tax distribution
    tax.invoice_repartition_line_ids = [
        (0, 0, {'repartition_type': 'base'}),
        (0, 0, {'repartition_type': 'tax', 'factor': 0.5, 'account_id': liability_account.id}),
        (0, 0, {'repartition_type': 'tax', 'factor': 0.5, 'account_id': income_account.id}),
    ]
    
    # 4. Create products
    print("\n4. Creating products...")
    
    # POS product
    pos_product = env['product.product'].create({
        'name': 'Meat Plate',
        'detailed_type': 'consu',
        'list_price': 100,
        'available_in_pos': True,
        'taxes_id': [(6, 0, [tax.id])],
        'company_id': company.id,
    })
    print(f"   ✓ {pos_product.name} - ${pos_product.list_price}")
    
    # Room product
    room_product = env['product.product'].create({
        'name': 'Standard Room',
        'detailed_type': 'service',
        'list_price': 3000,
        'available_in_pos': False,
        'company_id': company.id,
    })
    print(f"   ✓ {room_product.name} - ${room_product.list_price}")
    
    # 5. Create POS config
    print("\n5. Creating POS configuration...")
    pos_config = env['pos.config'].create({
        'name': 'Hotel Restaurant POS',
        'module_pos_hr': True,
        'is_restaurant': True,
        'company_id': company.id,
    })
    print(f"   ✓ {pos_config.name}")
    
    # 6. Create employee
    print("\n6. Creating employee...")
    employee = env['hr.employee'].create({
        'name': 'Waiter 1',
        'company_id': company.id,
    })
    print(f"   ✓ {employee.name}")
    
    # 7. Try to create room if Hotel PMS is installed
    print("\n7. Checking Hotel PMS...")
    try:
        # Create room type
        room_type = env['hotel.room.type'].create({
            'name': 'Standard',
            'product_id': room_product.id,
            'company_id': company.id,
        })
        
        # Create room
        room = env['hotel.room'].create({
            'name': '101',
            'room_type_id': room_type.id,
            'state': 'available',
            'housekeeping_state': 'clean',
            'company_id': company.id,
        })
        print(f"   ✓ Room 101 created")
    except Exception as e:
        print(f"   ⚠ Could not create room (Hotel PMS may not be fully installed): {e}")
    
    # Commit
    cr.commit()
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETED!")
    print("=" * 60)
    print("\nNext: Start Odoo and go to http://localhost:8069")