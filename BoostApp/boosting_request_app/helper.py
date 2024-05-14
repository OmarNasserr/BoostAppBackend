from divisions_app.models import Division


class BoostingRequestHelper:
    @staticmethod
    def get_price(current_div, desired_div):
        price = 0
        while current_div.id != desired_div.id:
            price += desired_div.price
            if desired_div.previous_division:
                desired_div = Division.objects.get(id=desired_div.previous_division.id)
            else:
                break

        return price
