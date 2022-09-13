from utils import prediction_random_images
import requests
import streamlit as st


def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict(file):
    # if request.method == 'POST':
    #     file = request.files.get('file')
    #     print(request.files)
    #     if file is None or file.filename == "":
    #         return jsonify({'error': 'no file'})
    #     if not allowed_file(filename=file.filename):
    #         return jsonify({'error': 'format not supported.'})

    if file:
        prediction = prediction_random_images([file.getvalue()])
        print(prediction)
        url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + \
            prediction.replace("_", "")
        res = requests.get(url)
        res_data = res.json()
        return {
            "recipeName": prediction,
            "other": res_data
        }


def cards(data):
    keys = data.keys()
    newDict = {}
    for key in keys:
        if data[key] is not None:
            newDict[key] = data[key]
    base = "strIngredient"
    ingredients = []
    amount = []
    for i in range(1, 21):
        ingredients.append(base+str(i))
        amount.append("strMeasure"+str(i))
    all_ingredients = ""
    st.subheader("Dish Name: {}".format(newDict["strMeal"]))
    st.text("Necessary Ingredients: ")

    for item in range(0, 20):
        if newDict.get(ingredients[item], False) and newDict[ingredients[item]] != "":
            curr = "* **{}** (`{}`)\n".format(
                newDict[ingredients[item]].capitalize(), newDict[amount[item]])
            all_ingredients += curr

    st.markdown(all_ingredients)
    st.caption("How to Cook: \n")
    st.markdown(data["strInstructions"])
    st.caption("Turorial: ")
    st.video(data=data["strYoutube"])


if __name__ == '__main__':
    st.header("EfficientNet (Based on Food-101 DataSet)", anchor=None)
    st.markdown('The current model has `92%` validation accuracy. Model can classify food items belongs to *Food-101* dataset classes.', unsafe_allow_html=True)
    file = st.file_uploader(label="Upload image (JPG, JPEG Only)")
    if file:
        _predict = predict(file)
        st.image(file)
        food_name = _predict["recipeName"].replace("_", " ")
        st.markdown('Model classified as: `{}`'.format(food_name))
        if _predict["other"]["meals"]:
            more_data = _predict["other"]["meals"]
            st.subheader("Found {} recipe for {}".format(
                len(more_data), food_name))
            for item in more_data:
                cards(item)
