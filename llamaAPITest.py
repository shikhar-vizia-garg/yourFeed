import replicate
from parseYoutubeVideoUtils import fetch_transcript
from gmailAPITest import read_emails_test , authenticate
import json
def fetch_posts_from_video(transcript):
    if len(transcript) > 500:
        return "Sorry Try Again!"

    transcript_str = ''
    for line in transcript:
        transcript_str = transcript_str + '\n' +line["text"]

    num_posts = int(max(4,(int(len(transcript_str)/2000)) * 1));
    print(len(transcript_str))
    print(num_posts)

    model_name = "meta/meta-llama-3-8b-instruct"
    system_prompt = "You are a professional content creator and a master at breaking down any content into multiple series of posts. All output must be in valid JSON. Only JSON. No prefix no suffix. Don’t add explanation beyond the JSON"
    prompt = '''
                \n\nDetermine the genre of the content. 
                Recommend image effect for this genre.
                Create {} posts using the content where each post is not more than 100 words long.
                With each post I want to generate an image using diffusion model , so recommend a prompt.
                Give the output in json using the output format given below:\n\n"
            '''.format(num_posts)
    response_format = '''
    {   
        "Genre":"<Genre1>,<Genre2>,<Genre3>",
        "imageEffect":"<effect1>,<effect2>,<effect3>",
        "posts":[
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
        ]
    } 
    '''

    # print(transcript_str)
    # print(len(transcript_str))

    input = {
        "prompt": transcript_str + prompt + response_format,
        "system_prompt": system_prompt
    }

    output = replicate.run(
        model_name,
        input=input
    )
    out = "".join(output)
    # print(out)
    return out

def fetch_posts_from_video_2(transcript):
    if len(transcript) > 500:
        return "Sorry Try Again!"

    transcript_str = ''
    for line in transcript:
        transcript_str = transcript_str + '\n' +line["text"]

    num_posts = int(max(4,(int(len(transcript_str)/2000)) * 2));
    print(len(transcript_str))
    print(num_posts)

    model_name = "meta/meta-llama-3-8b-instruct"
    # model_name = "meta/meta-llama-3-70b-instruct"
    # model_name = "meta/llama-2-13b"
    # system_prompt = "You are a professional content creator on twitter/X and is a master at converting any content into twitter/X posts."
    # prompt = "\n\n Convert the given video transcript content into a twitter thread of 5 posts where each post is no more than 60 words"
    system_prompt = "You are a professional content creator on twitter/X and is a master at converting any content into twitter/X posts.All output must be in valid JSON. Don’t add explanation beyond the JSON"
    prompt = '''
                \n\nDetermine the genre of the content. 
                Recommend image effect for this genre.
                Create {} post twitter thread using the content where each post is not more than 70 words long.
                With each twitter post I want to generate an image using diffusion model , so recommend a prompt.
                Give the output in json using the output format given below:\n\n"
            '''.format(num_posts)
    response_format = '''
    {   
        "Genre":"<Genre1>,<Genre2>,<Genre3>",
        "imageEffect":"<effect1>,<effect2>,<effect3>",
        "posts":[
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
        ]
    } 
    '''

    # print(transcript_str)
    # print(len(transcript_str))

    input = {
        "prompt": transcript_str + prompt + response_format,
        "system_prompt": system_prompt
    }

    output = replicate.run(
        model_name,
        input=input
    )
    out = "".join(output)
    # print(out)
    return out

def fetch_posts_from_mail(mail_body):
    # print(mail_body)
    # print(len(mail_body))
    if len(mail_body) > 20000:
        return "Sorry Try Again!"

    model_name = "meta/meta-llama-3-8b-instruct"
    system_prompt = ("You are a professional content creator on twitter/X and is a master at converting newsletter content into twitter/X posts."
                     "Newsletters contain promotional content , ads content and the main content. You should just analyse the main content"
                     "All output must be in valid JSON. Don't add any preceding message or any ending message , just output JSON.Don’t add explanation beyond the JSON")
    prompt = '''
                \n\nDetermine the genre of the content. 
                Recommend image effect for this genre.
                Create 5 post twitter thread using the content where each post is not more than 250 characters long.
                With each twitter post I want to generate an image using diffusion model , so recommend a prompt.
                Give the output in json using the output format given below:\n\n"
            '''
    response_format = '''
    {   
        "Genre":"<Genre1>,<Genre2>,<Genre3>",
        "imageEffect":"<effect1>,<effect2>,<effect3>",
        "posts":[
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
            {
                "post":"",
                "prompt::"",
            },
        ]
    } 
    '''
    input = {
        "prompt": mail_body + prompt + response_format,
        "system_prompt": system_prompt
    }

    output = replicate.run(
        model_name,
        input=input
    )
    out = "".join(output)
    return out

if __name__ == "__main__":
    video_id = "pTTkM-NHylw"
    start_seconds = 0
    end_seconds = 900
    transcript = fetch_transcript(video_id, start_seconds, end_seconds)
    posts = fetch_posts_from_video(transcript)
    print(posts)

    # mail_ids = [
    #     # "angad@mail.productmonk.io",
    #     "thesignaldaily@substack.com",
    #     # "theodore@whiteboardcrypto.com",
    #     # "therundownai@mail.beehiiv.com"
    # ]
    # creds = authenticate()
    # for id in mail_ids:
    #     body = read_emails_test(creds,id)
    #     posts = fetch_posts_from_mail(body)
    #     print(posts)
    #     data = json.loads(posts)
    #     for p in data['posts']:
    #         print(p)
    #     print(data)

