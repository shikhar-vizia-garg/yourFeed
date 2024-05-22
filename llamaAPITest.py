import replicate
from parseYoutubeVideoUtils import fetch_transcript , getStringTranscript

def getOutputs(transcript_str,model_name ,system_prompt ,prompt, response_format ):
    outputs = []
    start = 0
    end = 4000
    flag = False
    while True:
        print('''start {} end {}'''.format(start,end))
        input = {
            "prompt": transcript_str[start:end] + prompt + response_format,
            "system_prompt": system_prompt
        }
        output = replicate.run(
            model_name,
            input=input,
        )
        out = "".join(output)
        outputs.append(out)
        print(out)
        if flag:
            break
        start = end - 1000
        end = min(len(transcript_str) - 1 ,end + 3000)
        if end == len(transcript_str) - 1:
            flag = True

    return outputs

def fetch_posts_from_video(transcript):
    transcript_str = getStringTranscript(transcript)
    num_posts = 2
    model_name = "meta/meta-llama-3-8b-instruct"
    system_prompt = "You are a professional content creator and a master at writing 100 words post given video transcript content into multiple series of posts. All output must be in valid JSON. Only JSON. No prefix no suffix. Don’t add explanation beyond the JSON"
    prompt = '''
                    \n\nDetermine the genre of the content. 
                    Recommend image effect for this genre.
                    Create {} posts using the content where each post is not more than 100 words long. If needed use information from the internet. There should be logical coherence between the content with a clear begining and clear ending.
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
    outputs = getOutputs(transcript_str,model_name,system_prompt,prompt,response_format)
    print(outputs)
    return outputs
def fetch_posts_from_video_general(transcript):
    transcript_str = getStringTranscript(transcript)
    num_posts = 2#getNum(transcript_str)
    model_name = "meta/meta-llama-3-8b-instruct"
    system_prompt = "You are a professional content creator and a master at writing 100 words post given video transcript content into multiple series of posts. All output must be in valid JSON. Only JSON. No prefix no suffix. Don’t add explanation beyond the JSON"
    prompt = '''
                \n\nDetermine the genre of the content. 
                Recommend image effect for this genre.
                Create {} posts using the content where each post is not more than 100 words long. If needed use information from the internet. There should be logical coherence between the content with a clear begining and clear ending.
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
    outputs = getOutputs(transcript_str, model_name, system_prompt, prompt, response_format)
    return outputs

def getStringTranscript(transcript):
    transcript_str = ''
    for line in transcript:
        transcript_str = transcript_str + '\n' + line["text"]
    return transcript_str
def fetch_posts_from_video_instructional(transcript):
    if len(transcript) > 50000:
        return "Sorry Try Again!"

    transcript_str = ''
    for line in transcript:
        transcript_str = transcript_str + '\n' +line["text"]

    print(len(transcript_str))

    model_name = "meta/meta-llama-3-8b-instruct"
    system_prompt = ("You are a professional content creator and expert at writing instructional content. You would be give a video transcript of a intructional video and you would have to write an instructional textual content for the same.\n"
                     "All output must be in valid JSON.\n"
                     "Only JSON. No prefix no suffix. Don’t add explanation beyond the JSON")
    prompt = '''
                \n\n
                Understand the video transcript and do the following:
                1. Create one whatsapp message clearly listing out instructions in bullet points.\n
                2. For this message I want to generate an image using diffusion model , so recommend a prompt.\n
                Always give the output in json using the output format given below:\n\n"
            '''
    response_format = '''
    {   
        "post":"",
        "prompt":"",
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
        input=input,
    )
    out = "".join(output)
    print(out)
    return out

def fetch_posts_from_video_old(transcript):
    if len(transcript) > 50000:
        return "Sorry Try Again!"

    transcript_str = ''
    for line in transcript:
        transcript_str = transcript_str + '\n' +line["text"]

    num_posts = int(max(4,(int(len(transcript_str)/5000)) * 1));
    # print(len(transcript_str))
    # print(num_posts)

    model_name = "meta/meta-llama-3-8b-instruct"
    system_prompt = "You are a professional content creator and a master at writing 100 words post given video transcript content into multiple series of posts. All output must be in valid JSON. Only JSON. No prefix no suffix. Don’t add explanation beyond the JSON"
    prompt = '''
                \n\nDetermine the genre of the content. 
                Recommend image effect for this genre.
                Create {} posts using the content where each post is not more than 100 words long. If needed use information from the internet. There should be logical coherence between the content with a clear begining and clear ending.
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
    posts = fetch_posts_from_video_old(transcript)
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

