from urllib.parse import urlparse, urlunparse

def query_top_and_skip(output_data, query_pieces, my_members):
    top_count = int(query_pieces.get('$top',[str(len(my_members))])[0])
    top_skip = int(query_pieces.get('$skip',['0'])[0])
    my_members = my_members[top_skip:]
    
    if top_count < len(my_members):
        my_members = my_members[:top_count]
        query_out = {'$skip': top_skip + top_count, 'top':top_count}
        query_string = '&'.join(['{}={}'.format(k,v) for k,v in query_out.items()])
        output_data['Members@odata.nextLink'] = urlunparse(('','',path,'',query_string,''))
    else:
        pass

    return output_data
