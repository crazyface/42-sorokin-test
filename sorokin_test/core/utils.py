class order_by(object):

    def __init__(self, ordering=[], allowed=[], *args, **kwargs):
        #remove not allowed ordering
        self.ordering = filter(lambda x: x.strip('-') in allowed, ordering)
        print self.ordering
        self.positive_ordering = [x.strip('-') for x in self.ordering]

        self.links = {}
        self.remove = {}
        for order in allowed:
            val = order.strip('-')
            self.links[val] = self.for_link(val)
            self.remove[val] = self.remove_order(val)

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
        return '?' + '&'.join(query)

    def remove_order(self, value):
        query = []
        for order in self.ordering:
            print  value, order
            if value not in order:
                query.append('ordering=' + order)
        query = '?' + '&'.join(query)
        if value in self.positive_ordering:
            return {'need': True, 'query': query}
        return {'need': False, 'query': query}

    def get_current_order(self):
        order = '&'.join(['ordering=' + x for x in self.ordering])
        if order:
            return '?' + order
        return ''
