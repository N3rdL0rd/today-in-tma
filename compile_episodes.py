import os
import json
import frontmatter
from datetime import date

def compile_statements_to_json():
    """
    Parses all Markdown files and compiles relevant frontmatter
    into a single statements.json file.
    """
    statements_data = []
    transcript_dir = 'magnus_archives_transcripts/_posts'

    if not os.path.exists(transcript_dir):
        print(f"Directory '{transcript_dir}' not found. Please create it and add your transcripts.")
        return

    print(f"Scanning directory: {transcript_dir}")
    for filename in os.listdir(transcript_dir):
        if not (filename.endswith('.md') or filename.endswith('.markdown')):
            continue

        filepath = os.path.join(transcript_dir, filename)
        try:
            post = frontmatter.load(filepath)

            # Ensure the post has a statement date to be included
            if 'statement_date' in post.metadata and post.metadata['statement_date']:
                # Ensure the statement_date is a proper date string
                statement_date_val = post.metadata['statement_date']
                if isinstance(statement_date_val, date):
                    statement_date_str = statement_date_val.isoformat()
                else:
                    statement_date_str = str(statement_date_val).split(' ')[0]


                statement_info = {
                    'title': post.metadata.get('title', 'No Title'),
                    'episode_number': post.metadata.get('episode_number'),
                    'statement_date': statement_date_str,
                    'statement_of': post.metadata.get('statement_of'),
                    'summary': post.metadata.get('summary', 'No summary available.'),
                    'wiki_url': post.metadata.get('wiki_url')
                }
                statements_data.append(statement_info)

        except Exception as e:
            print(f"Could not process {filename}: {e}")

    # Sort statements by date for a well-ordered JSON file
    statements_data.sort(key=lambda x: x['statement_date'])

    # Write the data to a JSON file
    output_filename = 'out/statements.json'
    os.makedirs("out", exist_ok=True)
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(statements_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully compiled {len(statements_data)} statements into {output_filename}.")

if __name__ == '__main__':
    compile_statements_to_json()