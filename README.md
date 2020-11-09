# Feature extractor - Marketer

Python REST api for real estate properties text descriptions.
Capable of extracting syntactic features for given nouns of interest and comparing similarities between each real estate description.

## Installation

1. Clone repo and `cd` inside

2. Ensure you activated virtual env by: `source ./venv/bin/activate`

3. Install requirements: `pip install -r requirements.txt`

4. Install main package from project root: `pip install -e .`

5. Run `./marketer/api/api.py` and use 
    * `/extract` takes json consisting list of texts and nouns groups dict and returnes 
    * `/compare` takes the same set of data as `/extract` (json consisting list of texts and nouns groups dict) 
    but returns dict conatining 2 features similarity metrics `features_averaged_cosine_similarities`, `features_averaged_euclidean_similarities`
    and 1 text similarity metric `text_descriptions_similarities` 

6. Test by simply `pytest` from project root


Sample `/extract` curl with all texts and nouns groups:

```
curl --location --request POST 'http://localhost:5000/extract' \
--header 'Content-Type: application/json' \
--data-raw '{
    "texts": [
        "A spacious and rather elegant raised ground floor two bedroom apartment with two bathrooms (one en-suite) on this historic garden square, set within this wonderful stucco fronted property. The apartment has been decorated in a contemporary style, and features herringbone wood flooring in the reception areas and provides flexible accommodation with a generous reception space, perfect for both formal and informal entertaining. St George'\''s Square is a highly sought after central London location. It is moments from Pimlico Underground, with the local amenities and transport facilities of Victoria Station conveniently nearby.\nTwo bedrooms, Two bathrooms, Spacious accommodation, Close to excellent transport links, Garden Square location",
        "A spacious maisonette presented in immaculate condition having been intelligently re- designed. The property is arranged over the first, second and third floors with similar dimensions and feel to a house and looks over a quiet and secluded Mews to the rear. The accommodation briefly comprises; A top floor Reception room with large roof terrace, a separate kitchen, two double bedrooms, a third bedroom / Dining Room, two bathrooms and a private entrance. Warwick Way is positioned in a Central Pimlico location with a diverse range of amenities, including Victoria Mainline Station and Underground which are within a few minutes'\'' walk. The West End and Sloane Square are also easily accessible from this highly desirable central London address. Long Lease (900+ years), 2 / 3 bedrooms, Dining Room, Reception room, Kitchen, Terrace, Private front door entrance",
        "A newly refurbished and contemporary apartment located on the 3rd floor (with lift) of this centrally located building within the popular Portman Village on Upper Berkeley Street. The accommodation briefly comprises; Two double bedrooms (one en suite), a further family bathroom, a separate kitchen, and large and very open reception room. This wonderful apartment is situated within the popular Portman Village, with easy access to Marylebone High Street, Marble Arch, Oxford Circus and the green open spaces of Hyde Park. 2 bedrooms, 2 bathrooms, Long Lease, 3rd floor, Lift, Period, Portman Village, Central Location",
        "A delightful four bedroom Edwardian family home in excellent decorative order. The property has been beautifully refurbished and fully extended offering generous proportions and over 1600 square feet of living space. On the ground floor the accommodation provides a light-filled reception room and a downstairs W/C, followed by a substantial open-plan kitchen/dining room with bi-fold doors leading out to a wonderful garden. The first and second floors provide four bedrooms and two bathrooms (one en-suite). The house has been very well designed and is in excellent decorative order throughout.\nSummerlands Avenue is very well located providing easy access to both the A40 and M4. The property is within a short walk of Acton Park, Acton Main Line (forthcoming Crossrail link) and Acton Central (London Overground) station. There are an abundance of schools nearby including Derwentwater, Ark Byron, Ark Priory and St. Vincent'\''s Primary Schools and Twyford Church of England Secondary School. Edwardian, Terraced, Four Bedrooms, Two Bathrooms, Two Receptions, Open-Plan Kitchen/Dining Room, W/C, Garden",
        "A handsome and substantial six bedroom semi-detached Edwardian family house. The property provides a wealth of period features and offers excellent proportions measuring over 2400 sq.ft. On the ground floor, the charming hallway with original tiled flooring leads to a front reception, a kitchen/breakfast room, and a dining room with French doors which open out to an attractive 50 ft garden. On the first floor there is a master bedroom with an en-suite shower room, a family bathroom and three further bedrooms. The second floor has been generously converted offering two double bedrooms and an additional bathroom as well as plenty of useful eaves storage space. The property offers further potential for a rear and side-return extension subject to planning permission. The house is situated in a popular location within a short walk from West Acton (Central line) and Ealing Common (District line) stations. The property also provides easy access to the forthcoming Crossrail link Acton Main Line (Elizabeth line) station and the A40/A4/M4. Local schools include Twyford CofE High School, St. Vincent'\''s Primary School, Berrymede Infant School and Derwentwater Primary School. Edwardian, Semi-Detached, Six Bedrooms, Two Receptions Rooms, Kitchen/Breakfast Room, Three Bathrooms, Garden"
    ],
    "nouns_groups": {
        "bathroom": [
            "bathroom",
            "bath"
        ],
        "bedroom": [
            "bedroom"
        ],
        "living room": [
            "living room",
            "reception",
            "reception room",
            "receptions room",
            "reception area",
            "reception space"
        ],
        "property": [
            "property",
            "apartment",
            "maisonette",
            "house",
            "accommodation",
            "home"
        ],
        "garden": [
            "garden",
            "yard"
        ],
        "location": [
            "location"
        ],
        "transport": [
            "transport",
            "transport link"
        ]
    }
}
```