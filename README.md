# Banking-Software-
 A secure GUI-based banking management system built with Python and Tkinter
 
# Custom Banking Software

A secure GUI-based banking management system built with Python and Tkinter.

## Features

- **Account Management**
  - Create new customer accounts with auto-generated account numbers
  - View account details and balance
  - Modify customer information (name, phone, address, age)
  - Delete accounts

- **Transactions**
  - Deposit money (with transaction limits: ₹1,000 - ₹200,000,000)
  - Withdraw money (with balance verification)
  - Real-time balance updates

- **Account Types**
  - Savings Account
  - Checking Account

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.x
- MySQL Server
- Required Python packages (see Installation section)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/banking-software.git
   cd banking-software
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database**
   - Install MySQL Server on your system
   - Start the MySQL service
   - Update the database credentials in the code if needed (default: user="root", passwd="tiger")

4. **Add the secure.png image**
   - Place a `secure.png` image file in the project root directory
   - Recommended size: 150x150 pixels or larger

## Usage

1. Run the application:
   ```bash
   python banking_software.py
   ```

2. The main window will display with the following options:
   - **New Account**: Create a new customer account
   - **Check Balance**: View account details and balance
   - **Modify Account**: Update customer information
   - **Withdraw Money**: Make withdrawals from an account
   - **Deposit Money**: Deposit funds into an account
   - **Delete Account**: Remove an account from the system

## Database Structure

The application automatically creates a database named `project` with the following table:

**Customer Table**
- `accno` (INT, Primary Key): Account number
- `name` (VARCHAR(50)): Customer name
- `contactno` (VARCHAR(10)): Phone number
- `address` (VARCHAR(100)): Residential address
- `acc_type` (VARCHAR(20)): Account type (Savings/Checking)
- `age` (INT): Customer age
- `balance` (INT): Account balance

## Security Features

- Auto-generated 6-digit account numbers
- Transaction limit enforcement
- Balance verification before withdrawals
- Confirmation dialogs for critical operations


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

ritvikverma8

## Acknowledgments

- Built with Python Tkinter
- MySQL for database management
- PIL (Pillow) for image handling

## Future Enhancements

- [ ] Add user authentication
- [ ] Implement transaction history
- [ ] Add account statements generation
- [ ] Include interest calculation
- [ ] Add password protection for accounts
- [ ] Export reports to PDF/Excel
