import os
import argparse
import aiohttp
import asyncio
from weather_etl import *
from country import * 
import time


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

async def get(url, session):
    try:
        async with session.get(url=url) as response:
            # resp = await response.read()
            # print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
            return await response.text()
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def main(urls):
    async with aiohttp.ClientSession(headers=headers) as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))
    return ret


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--country", type=str, default=None)
    parser.add_argument("-s","--state", type=str, default=None)
    parser.add_argument("-rs","--return_state", type=str2bool, default=False)
    parser.add_argument("-rc","--return_city", type=str2bool,  default=False)
    args = vars(parser.parse_args())
  
    country_name = args['country']
    state_name = args['state']
    return_state = args['return_state']
    return_city = args['return_city']
   
    location = country_name.lower() if country_name else '' 
    location += f"_{state_name.lower()}" if state_name else ''
    
    strt_time = time.time()

    urls = extract_data_urls(country_name, 
                 state_name, 
                 return_state, 
                 return_city)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(urls.values()))
    results = [json.loads(result) for result in results]
    results_dict = dict(zip(urls.keys(),results))
    transform_load_data_to_df(results_dict, region=location)
  
    print(time.time() - strt_time)