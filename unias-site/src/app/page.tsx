import type {NextPage} from 'next';
import Head from 'next/head';
import Uniai from '../../components/unias';
import styles from './Home.module.css';

const Home: NextPage = () => {
    return (
        
        <div className={styles.container}>
            <Head>
            <main>
                <Uniai />
            </main>
            </Head>
            <Uniai />
        </div>
        
    );
}

export default Home;