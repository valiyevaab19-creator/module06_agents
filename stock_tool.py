class StockLookup:
    """A tool that knows how many products are in stock."""

    def __init__(self, stock):
        # Store the product counts.
        self.stock = stock

    def find_product(self, text):
        # Look for the first known product mentioned in the message.
        for product in self.stock:
            if product.lower() in text.lower():
                return product
        return None

    def count_for(self, product):
        # Return the quantity for the product, or None if it is unknown.
        if product in self.stock:
            return self.stock[product]
        return None
