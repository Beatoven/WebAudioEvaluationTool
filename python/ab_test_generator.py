# Script for dynamically generating test pages. Ensure that 
# audio filenaming follows this format: 0_A.wav, 0_B.wav,
# 1_A.wav, 1_B.wav, etc. and are saved in a dir and are
# saved in a directory called eval_audio/


import xml.etree.ElementTree as ET
import argparse
import os

# os.chdir("./evaluation/WebAudioEvaluationTool/")

def load_and_append_xml(xml_path, additional_xml):
    # Load the XML document
    xml_path = os.path.abspath(xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Append additional XML
    additional_root = ET.fromstring(additional_xml)
    root.extend(additional_root)
    
    # Return the modified XML tree
    return tree

def generate_test_pages(num_pages, audio_path, outside_ref=False):
    xml = '<root>'  # Add a root element
    for i in range(1, num_pages):
        xml += f'<page id="test-{i}" hostURL="{audio_path}" randomiseOrder="true" repeatCount="0" loop="false"\n'
        xml += '    synchronous="false" loudness="0" label="default" labelStart="" poolSize="0"\n'
        xml += '    alwaysInclude="false" preSilence="0" postSilence="0" playOne="false"\n'
        xml += '    restrictMovement="false" minNumberPlays="0">\n'
        xml += '    <commentboxprefix>Comment on track</commentboxprefix>\n'
        xml += '    <interface />\n'
        xml += f'    <audioelement url="{i}_A.wav" id="track-{2*i}" gain="0" label="" type="normal"\n'
        xml += '        alwaysInclude="false" preSilence="0" postSilence="0" minNumberPlays="0" />\n'
        xml += f'    <audioelement url="{i}_B.wav" id="track-{2*i+1}" gain="0" label="" type="normal"\n'
        xml += '        alwaysInclude="false" preSilence="0" postSilence="0" minNumberPlays="0" />\n'
        if outside_ref:
            xml += f'    <audioelement url="{i}_X.wav" id="ref-{2*i}" gain="0" type="outside-reference" />\n'
        xml += '    <survey location="pre" showBackButton="true" />\n'
        xml += '    <survey location="post" showBackButton="true" />\n'
        xml += '</page>\n'
    xml += '</root>'  # Close the root element
    return xml

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    print(os.getcwd())
    parser.add_argument("--xml_path", default="./python/base_test_template.xml", help="Path to the XML file (default: %(default)s)")
    parser.add_argument("--audio_path", default="eval_audio/", help="Path to audio files to be evaluated (default: %(default)s)")
    parser.add_argument("--ref", default=False, help="Whether or not to include reference audio as part of the test (e.g., 1_X.wav)")
    parser.add_argument("--num_pages", type=int, required=True, help="Number of additional pages to add")
    parser.add_argument("--test_title", type=str, required=True, help="Name of evaluation experiment")
    args = parser.parse_args()
    # args.xml_path = "./python/base_test_template.xml"
    # args.num_pages = 20
    # args.test_title = "beatoven_ab_template"

    test_pages = generate_test_pages(args.num_pages, args.audio_path, args.ref)
    # Load base xml and append test pages
    updated_test_xml = load_and_append_xml(args.xml_path, test_pages)

    # # Save the modified XML content to a file
    save_dir = os.path.join("tests",args.test_title)
    updated_test_xml.write(save_dir+".xml")


