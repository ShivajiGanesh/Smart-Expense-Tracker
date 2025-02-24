{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "4ee02280-877e-463b-bae3-526e4a1a7886",
   "metadata": {},
   "outputs": [
    {
     "ename": "ValueError",
     "evalue": "The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "\u001b[1;32m~\\AppData\\Local\\Temp\\ipykernel_17004\\2351356039.py\u001b[0m in \u001b[0;36m?\u001b[1;34m()\u001b[0m\n\u001b[0;32m     19\u001b[0m     \u001b[0mplt\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mshow\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     20\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     21\u001b[0m \u001b[1;31m# Testing visualization\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     22\u001b[0m \u001b[1;32mif\u001b[0m \u001b[0m__name__\u001b[0m \u001b[1;33m==\u001b[0m \u001b[1;34m\"__main__\"\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 23\u001b[1;33m     \u001b[0mplot_expense_distribution\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;32m~\\AppData\\Local\\Temp\\ipykernel_17004\\2351356039.py\u001b[0m in \u001b[0;36m?\u001b[1;34m()\u001b[0m\n\u001b[0;32m      7\u001b[0m \u001b[1;32mdef\u001b[0m \u001b[0mplot_expense_distribution\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      8\u001b[0m     \u001b[0mexpenses\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mdatabase\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mget_expenses\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 9\u001b[1;33m     \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[0mexpenses\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     10\u001b[0m         \u001b[0mprint\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"No data available for visualization.\"\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     11\u001b[0m         \u001b[1;32mreturn\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     12\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\anaconda3\\lib\\site-packages\\pandas\\core\\generic.py\u001b[0m in \u001b[0;36m?\u001b[1;34m(self)\u001b[0m\n\u001b[0;32m   1575\u001b[0m     \u001b[1;33m@\u001b[0m\u001b[0mfinal\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1576\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0m__nonzero__\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m)\u001b[0m \u001b[1;33m->\u001b[0m \u001b[0mNoReturn\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m-> 1577\u001b[1;33m         raise ValueError(\n\u001b[0m\u001b[0;32m   1578\u001b[0m             \u001b[1;34mf\"The truth value of a {type(self).__name__} is ambiguous. \"\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1579\u001b[0m             \u001b[1;34m\"Use a.empty, a.bool(), a.item(), a.any() or a.all().\"\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1580\u001b[0m         )\n",
      "\u001b[1;31mValueError\u001b[0m: The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all()."
     ]
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import database  # Import database functions\n",
    "\n",
    "def plot_expense_distribution():\n",
    "    expenses = database.get_expenses()  # Fetch expenses from database.py\n",
    "    \n",
    "    if expenses.empty:  # Correct way to check if DataFrame is empty\n",
    "        print(\"No data available for visualization.\")\n",
    "        return\n",
    "\n",
    "    plt.figure(figsize=(8, 5))\n",
    "    sns.barplot(x=\"category\", y=\"amount\", data=expenses)\n",
    "    plt.title(\"Expense Distribution by Category\")\n",
    "    plt.xticks(rotation=45)\n",
    "    plt.show()\n",
    "\n",
    "# Testing visualization\n",
    "if __name__ == \"__main__\":\n",
    "    plot_expense_distribution()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d23a89df-e850-4d97-a872-157c0b52d84e",
   "metadata": {},
   "outputs": [],
   "source": []
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
