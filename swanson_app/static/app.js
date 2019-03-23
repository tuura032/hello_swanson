'use strict';

const e = React.createElement;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
        error: null,
        isLoaded: false,
        items: []
    };
  }

  componentDidMount() {
    //const proxyurl = "https://cors-anywhere.herokuapp.com/";
    const url = "https://hello-swanson.herokuapp.com/api/quote";
    fetch(url)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result // was result.items, referencing data.json
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  callApi(size) {
    const url = 'https://hello-swanson.herokuapp.com/api/'
    fetch(url + size)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result // was result.items, referencing data.json
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  vote(rating) {
    fetch('https://hello-swanson.herokuapp.com/api/rating', {
        method: 'POST',
        headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({
        user_rating: rating,
        quote_id: this.state.items.id
        }),
    });
  }
  
  render() {
    const { error, isLoaded, items } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
        return (
            <div className="quote-box">
                <h2>{ items.quote }</h2>
                <h4>- { items.author }</h4>
                <h4> {items.word_count}</h4>
                <h4> QID {items.id}</h4>
                <h4>Rating: {items.average_rating} / 5</h4>
                <button onClick={() => {this.callApi('quote')}}>
                    Click here to get a random quote!
                </button>
                <br />
                <button onClick={() => {this.callApi('large')}}>
                Big Quote
                </button>
                <button onClick={() => {this.callApi('medium')}}>
                Medium Quote
                </button>
                <button onClick={() => {this.callApi('small')}}>
                Small Quote
                </button>
                <br />
                <button onClick={() => {this.vote(1)}}>1 Star</button>
                <button onClick={() => {this.vote(2)}}>2 Stars</button>
                <button onClick={() => {this.vote(3)}}>3 Stars</button>
                <button onClick={() => {this.vote(4)}}>4 Stars</button>
                <button onClick={() => {this.vote(5)}}>5 Stars</button>
            </div>
            
        );
      }
    
    // if (this.state.liked) {
    //   return 'You liked this.';
    // }

    // // Display a "Like" <button>
    // return (
    //     <button onClick={() => this.setState({ liked: true })}>
    //         Get a quote!
    //     </button>
    // );
  }
}

const domContainer = document.querySelector('#app');
ReactDOM.render(e(App), domContainer);