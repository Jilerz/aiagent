import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    verbose = "--verbose" in sys.argv
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        function_results = []
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt,
                )
            )
        except errors.ClientError as e:
            print(f'Gemini API error: {e}')
            sys.exit(1)
            
        if response.candidates:
            for item in response.candidates:
                messages.append(item)
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        
        

        if args.verbose:
            print("User prompt:", args.user_prompt)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.function_calls:
            for call in response.function_calls:
                print(f'Calling function: {call.name}({call.args})')
                function_call_result = call_function(call,verbose=verbose)
                if not function_call_result.parts:
                    raise ValueError("function response parts is empty")
                parts = function_call_result.parts[0]
                if parts.function_response is None:
                    raise ValueError("Expected value in parts[0] function reponse, got None")
                if parts.function_response.response is None:
                    raise ValueError("Expected response, got None")
                
                function_results.append(parts)
                if verbose:
                    resp = parts.function_response.response  # dict
                    if "result" in resp:
                        print(f"-> {resp['result']}")
                    elif "error" in resp:
                        print(f"-> ERROR: {resp['error']}")
                    else:
                        print(f"-> {resp}")
                messages.append(
                    types.Content(
                        role="user",
                        parts=function_results,
                    )
                )
        else:
            return print("Response:"), print(response.text)
    print("Failure to resolve initial inquiry. response limit reached without final answer given.")
    sys.exit(1)
    
    
    
            
                     



if __name__ == "__main__":
    main()