{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "94b35084-30cb-4950-8bd6-0509e90abc82",
   "metadata": {},
   "outputs": [],
   "source": [
    "import database\n",
    "import analysis\n",
    "\n",
    "# Test database\n",
    "database.add_expense(\"Lunch\", 150, \"Food\")\n",
    "expenses = database.get_expenses()\n",
    "print(expenses)\n",
    "\n",
    "# Test visualization\n",
    "analysis.plot_expense_distribution()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.16"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
