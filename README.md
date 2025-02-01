# 📈 Stock Recommendation System 🚀

Welcome to the **Stock Recommendation System**, a web app that helps you make smarter investment decisions based on your **budget** and **risk level**! 💰

This system uses **real-time stock data** to suggest which stocks to buy, how many shares to invest in, and displays a graphical representation of stock price trends. 📊

---

## 🚀 Features

- 📉 **Stock Recommendation**: Get personalized stock suggestions based on your risk tolerance (low, medium, high).
- 💸 **Budget-Based Investment**: Suggests the number of stocks you can buy based on your budget.
- 🛡️ **Manipulation Detection**: Detects potential stock market manipulation to keep you safe! ⚠️
- 📅 **Custom Date Range**: Select any date range to view stock data over time.
- 📈 **Interactive Stock Graph**: View a stock's price trends visually with graphs 🖼️.
- 🔒 **Secure & Fast**: Built with FastAPI for a smooth and responsive experience.

---

## ⚙️ Technologies Used

- **Frontend**: React, CSS, JavaScript
- **Backend**: FastAPI, Python
- **Data Source**: Yahoo Finance (via `yfinance` library)
- **Data Visualization**: Matplotlib (for stock price graphs)

---

## 📲 How to Use

### 1. Install Dependencies

#### Frontend Setup

Navigate to the frontend folder and install the required dependencies:

- `cd frontend`
- `npm install`

Then, start the React development server:

- `npm start`

#### Backend Setup

Navigate to the backend folder and install the required Python dependencies:

- `cd backend`
- `pip install -r requirements.txt`

Start the FastAPI server:

- `uvicorn main:app --reload`

The backend will be running at `http://localhost:8000`.

### 2. Access the App

- Open your browser and visit `http://localhost:3000` for the frontend interface.
- The backend will be running at `http://localhost:8000`.

### 3. How It Works

Once you open the app, follow these steps to get your stock recommendations:

1. **Enter a Stock Ticker**: 
   - Type the stock ticker symbol (e.g., `AAPL` for Apple).
   
2. **Select a Date Range**: 
   - Choose the **start date** and **end date** for the period you're interested in.

3. **Select Your Risk Level**: 
   - Choose the risk level (`Low`, `Medium`, `High`) based on how much risk you're willing to take.

4. **Enter Your Budget**: 
   - Type your investment budget to see how many stocks you can afford.

5. **Click "Get Recommendation"**:
   - Once you've entered all the information, click the button to get the recommendation.

#### What You Get:
- **Stock Recommendation**: The app will suggest the number of stocks you should invest in.
- **Graph of Stock Prices**: The app displays a graphical representation of stock prices over the selected date range.
- **Manipulation Detection**: A warning will appear if manipulation is detected in the stock's data.

## 📊 Example Tickers

Here are some example stock tickers you can use to test the system:

- **Apple**: `AAPL`
- **Google**: `GOOGL`
- **Tesla**: `TSLA`

---


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

We welcome contributions and bug reports! If you want to suggest a feature or fix a bug, feel free to submit an issue or a pull request.

## 🙏 Acknowledgements

- **FastAPI**: A fast web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **yFinance**: A library to fetch historical stock data from Yahoo Finance.
- **Matplotlib**: A plotting library for creating static, animated, and interactive visualizations.
- **React**: A JavaScript library for building user interfaces.
- **Create React App**: A tool to set up a modern web app by running one command.
- **OpenAI's GPT-3**: For providing suggestions and answers throughout the development of this project.





