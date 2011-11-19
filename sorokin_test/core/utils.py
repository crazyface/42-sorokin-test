class order_by(object):

    def __init__(self, ordering=[], allowed=[], *args, **kwargs):
        #remove not allowed ordering
        self.ordering = filter(lambda x: x.strip('-') in allowed, ordering)
        #compute querystring for all allowed orders
        self.links = {}
        for order in allowed:
            val = order.strip('-')
            self.links[val] = self.for_link(val)

    def invert(self, value):
        if '-' in value:
            return value.strip('-')
        return '-' + value

    def for_link(self, value):
        """
        compute querystring whith "value order" on first place
        """
        query = []
        val = value
        for order in self.ordering:
            if value not in order:
                query.append('ordering=' + order)
            else:
                val = order
        query = ['ordering=' + self.invert(val)] + query
        return '&'.join(query)

    def get_current_order(self):
        return '&'.join(['ordering=' + x for x in self.ordering])
