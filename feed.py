import yaml
import xml.etree.ElementTree as ET

with open("feed.yaml", mode="r") as file:
    yaml_data = yaml.safe_load(file)

rss = ET.Element(
    "rss",
    {
        "version": "2.0",
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
    }
)

channel = ET.SubElement(rss, "channel")

base_url = yaml_data.get("base_url", "https://limitless-script.github.io/podcast/")

ET.SubElement(channel, "title").text = yaml_data.get("title")
ET.SubElement(channel, "format").text = yaml_data.get("format")
ET.SubElement(channel, "subtitle").text = yaml_data.get("subtitle")
ET.SubElement(channel, "itunes:author").text = yaml_data.get("author")
ET.SubElement(channel, "description").text = yaml_data.get("description")
ET.SubElement(channel, "base_url").text = base_url
ET.SubElement(channel, "itunes:image", {"href": base_url + yaml_data.get("image")})
ET.SubElement(channel, "language").text = yaml_data.get("language")
ET.SubElement(channel, "itunes:category", {"text": yaml_data.get("category")})

for item in yaml_data.get("item", []):
    item_element = ET.SubElement(channel, "item")
    ET.SubElement(item_element, "title").text = item.get("title")
    ET.SubElement(item_element, "itunes:author").text = yaml_data["author"]
    ET.SubElement(item_element, "description").text = item.get("description")
    ET.SubElement(item_element, "itunes:duration").text = item.get("duration")
    ET.SubElement(item_element, "published").text = item.get("published")

    enclosure = ET.SubElement(
        item_element, 
        "enclosure", 
        {
            "url": base_url + item.get("file"),
            "type": "audio.mpeg",
            "length": item.get("length")
        }
    )

tree = ET.ElementTree(rss)
tree.write("podcast.xml", encoding="utf-8", xml_declaration=True)
